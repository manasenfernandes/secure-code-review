import os
import sqlite3
from functools import wraps
from pathlib import Path

from flask import (
    Flask, request, redirect, url_for,
    session, flash, render_template_string
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configure application security
app.secret_key = os.environ.get("SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("Please configure the SECRET_KEY environment variable.")

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "false").lower() == "true"
)

DATABASE = Path(__file__).with_name("auth.db")


# Database connection
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


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

        # Create an administrator using environment variables
        admin_username = os.environ.get("ADMIN_USERNAME")
        admin_password = os.environ.get("ADMIN_PASSWORD")

        if admin_username and admin_password:
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
            return "Enter a username and a password of at least 12 characters.", 400

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
            Username: <input name="username" required maxlength="50"><br><br>
            Password: <input name="password" type="password" required minlength="12"><br><br>
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

        with get_db() as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            ).fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(url_for("dashboard"))

        return "Invalid username or password.", 401

    return render_template_string("""
        <h2>Login</h2>
        <form method="POST">
            Username: <input name="username" required><br><br>
            Password: <input name="password" type="password" required><br><br>
            <button type="submit">Login</button>
        </form>
        <a href="/register">Register</a>
    """)


# User dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template_string("""
        <h2>User Dashboard</h2>
        <p>Welcome, {{ username }}!</p>
        <p>Your role: User</p>
        <form method="POST" action="/logout">
            <button type="submit">Logout</button>
        </form>
    """, username=session["username"])


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
