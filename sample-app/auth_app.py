import os
import sqlite3
import time
from contextlib import contextmanager
from functools import wraps
from pathlib import Path

from flask import (
    Flask, request, redirect, url_for,
    session, flash, render_template_string
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)

# Configure application security
app.secret_key = os.environ.get("SECRET_KEY")

if not app.secret_key:
    raise RuntimeError(
        "Please configure the SECRET_KEY environment variable."
    )

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=(
        os.environ.get("COOKIE_SECURE", "false").lower() == "true"
    ),
    MAX_LOGIN_ATTEMPTS=5,
    LOGIN_LOCKOUT_SECONDS=900
)

csrf = CSRFProtect(app)

DATABASE = Path(__file__).with_name("auth.db")


# Database connection with automatic closing
@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# Create database and tables
def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user'
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS login_attempts (
                username TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                failed_attempts INTEGER NOT NULL DEFAULT 0,
                first_attempt_at INTEGER NOT NULL,
                locked_until INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (username, ip_address)
            )
        """)

        # Create administrator using environment variables
        admin_username = os.environ.get("ADMIN_USERNAME")
        admin_password = os.environ.get("ADMIN_PASSWORD")

        if admin_username or admin_password:

            if not admin_username or not admin_password:
                raise RuntimeError(
                    "Both ADMIN_USERNAME and ADMIN_PASSWORD must be set."
                )

            if len(admin_username) > 50:
                raise RuntimeError(
                    "Administrator username must not exceed 50 characters."
                )

            if len(admin_password) < 12:
                raise RuntimeError(
                    "Administrator password must contain at least 12 characters."
                )

            existing_admin = conn.execute(
                "SELECT id FROM users WHERE username = ?",
                (admin_username,)
            ).fetchone()

            if not existing_admin:
                conn.execute(
                    """
                    INSERT INTO users (username, password_hash, role)
                    VALUES (?, ?, 'admin')
                    """,
                    (
                        admin_username,
                        generate_password_hash(admin_password)
                    )
                )


# Login-required decorator
def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("login"))

        return function(*args, **kwargs)

    return wrapper


# Admin-only decorator
def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("login"))

        with get_db() as conn:
            user = conn.execute(
                "SELECT role FROM users WHERE id = ?",
                (session["user_id"],)
            ).fetchone()

        if not user or user["role"] != "admin":
            return "Access Denied: Admin privileges required.", 403

        return function(*args, **kwargs)

    return wrapper


# Login rate-limiting helper
def is_login_locked(username, ip_address):
    current_time = int(time.time())

    with get_db() as conn:
        attempt = conn.execute(
            """
            SELECT failed_attempts, first_attempt_at, locked_until
            FROM login_attempts
            WHERE username = ? AND ip_address = ?
            """,
            (username, ip_address)
        ).fetchone()

        if not attempt:
            return False

        if current_time >= attempt["locked_until"] and (
            attempt["locked_until"] > 0
        ):
            conn.execute(
                """
                DELETE FROM login_attempts
                WHERE username = ? AND ip_address = ?
                """,
                (username, ip_address)
            )
            return False

        if current_time - attempt["first_attempt_at"] >= 900:
            conn.execute(
                """
                DELETE FROM login_attempts
                WHERE username = ? AND ip_address = ?
                """,
                (username, ip_address)
            )
            return False

        return attempt["locked_until"] > current_time


# Record failed login attempts
def record_failed_login(username, ip_address):
    current_time = int(time.time())

    with get_db() as conn:
        attempt = conn.execute(
            """
            SELECT failed_attempts, first_attempt_at
            FROM login_attempts
            WHERE username = ? AND ip_address = ?
            """,
            (username, ip_address)
        ).fetchone()

        if not attempt or current_time - attempt["first_attempt_at"] >= 900:
            conn.execute(
                """
                INSERT OR REPLACE INTO login_attempts
                (username, ip_address, failed_attempts,
                 first_attempt_at, locked_until)
                VALUES (?, ?, 1, ?, 0)
                """,
                (username, ip_address, current_time)
            )
            return 1

        failures = attempt["failed_attempts"] + 1

        locked_until = 0

        if failures >= app.config["MAX_LOGIN_ATTEMPTS"]:
            locked_until = (
                current_time + app.config["LOGIN_LOCKOUT_SECONDS"]
            )

        conn.execute(
            """
            UPDATE login_attempts
            SET failed_attempts = ?, locked_until = ?
            WHERE username = ? AND ip_address = ?
            """,
            (failures, locked_until, username, ip_address)
        )

        return failures


# Clear failed login attempts after successful login
def clear_login_attempts(username, ip_address):
    with get_db() as conn:
        conn.execute(
            """
            DELETE FROM login_attempts
            WHERE username = ? AND ip_address = ?
            """,
            (username, ip_address)
        )


# Home page
@app.route("/")
def home():

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return render_template_string("""
        <h2>Secure Code Review - Authentication</h2>
        <a href="/register">Register</a> |
        <a href="/login">Login</a>
    """)


# User registration
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or len(username) > 50 or len(password) < 12:
            return (
                "Enter a username and a password of at least 12 characters.",
                400
            )

        password_hash = generate_password_hash(password)

        try:
            with get_db() as conn:
                conn.execute(
                    """
                    INSERT INTO users (username, password_hash, role)
                    VALUES (?, ?, 'user')
                    """,
                    (username, password_hash)
                )

            flash("Registration successful. Please log in.")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            return "Username already exists.", 409

    return render_template_string("""
        <h2>Register</h2>
        <form method="POST">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
            Username: <input name="username" required maxlength="50"><br><br>
            Password: <input name="password" type="password"
                required minlength="12"><br><br>
            <button type="submit">Register</button>
        </form>
        <a href="/login">Login</a>
    """)


# User login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        ip_address = request.remote_addr or "unknown"

        if is_login_locked(username, ip_address):
            return (
                "Too many failed login attempts. Please try again later.",
                429
            )

        with get_db() as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            ).fetchone()

        if user and check_password_hash(user["password_hash"], password):

            clear_login_attempts(username, ip_address)

            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(url_for("dashboard"))

        failures = record_failed_login(username, ip_address)

        if failures >= app.config["MAX_LOGIN_ATTEMPTS"]:
            return (
                "Too many failed login attempts. Please try again later.",
                429
            )

        return "Invalid username or password.", 401

    return render_template_string("""
        <h2>Login</h2>
        <form method="POST">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
            Username: <input name="username" required maxlength="50"><br><br>
            Password: <input name="password" type="password" required><br><br>
            <button type="submit">Login</button>
        </form>
        <a href="/register">Register</a>
    """)


# User dashboard
@app.route("/dashboard")
@login_required
def dashboard():

    with get_db() as conn:
        user = conn.execute(
            "SELECT role FROM users WHERE id = ?",
            (session["user_id"],)
        ).fetchone()

    if not user:
        session.clear()
        return redirect(url_for("login"))

    return render_template_string("""
        <h2>User Dashboard</h2>
        <p>Welcome, {{ username }}!</p>
        <p>Your role: {{ role }}</p>
        <form method="POST" action="/logout">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
            <button type="submit">Logout</button>
        </form>
    """, username=session["username"], role=user["role"])


# Admin-only dashboard
@app.route("/admin")
@admin_required
def admin():

    with get_db() as conn:
        users = conn.execute(
            "SELECT id, username, role FROM users"
        ).fetchall()

    return render_template_string("""
        <h2>Administrator Dashboard</h2>
        <p>Welcome, {{ username }}!</p>
        <h3>Registered Users</h3>
        <ul>
        {% for user in users %}
            <li>{{ user["username"] }} - {{ user["role"] }}</li>
        {% endfor %}
        </ul>
        <form method="POST" action="/logout">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
            <button type="submit">Logout</button>
        </form>
    """, username=session["username"], users=users)


# Logout
@app.route("/logout", methods=["POST"])
@login_required
def logout():

    session.clear()
    flash("You have logged out.")

    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run(debug=False)
