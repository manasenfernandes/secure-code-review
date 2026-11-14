import os
import re
import sys
from pathlib import Path

import pytest

os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ADMIN_USERNAME", "testadmin")
os.environ.setdefault("ADMIN_PASSWORD", "test-admin-password")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import auth_app as auth


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DATABASE", tmp_path / "test_auth.db")
    monkeypatch.setenv("ADMIN_USERNAME", "testadmin")
    monkeypatch.setenv("ADMIN_PASSWORD", "test-admin-password")

    auth.app.config["TESTING"] = True
    auth.app.config["WTF_CSRF_ENABLED"] = True

    auth.init_db()

    with auth.app.test_client() as client:
        yield client


def get_csrf_token(client, page):
    response = client.get(page)
    assert response.status_code == 200

    match = re.search(
        r'name="csrf_token" value="([^"]+)"',
        response.get_data(as_text=True)
    )

    assert match is not None
    return match.group(1)


def register_user(
    client,
    username="testuser",
    password="secure-password-123"
):
    token = get_csrf_token(client, "/register")

    return client.post("/register", data={
        "username": username,
        "password": password,
        "csrf_token": token
    })


def login_user(client, username, password):
    token = get_csrf_token(client, "/login")

    return client.post("/login", data={
        "username": username,
        "password": password,
        "csrf_token": token
    })


# 1. Registration and password hashing
def test_registration_and_password_hashing(client):
    response = register_user(client)

    assert response.status_code == 302

    with auth.get_db() as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            ("testuser",)
        ).fetchone()

    assert user is not None
    assert user["password_hash"] != "secure-password-123"

    assert auth.check_password_hash(
        user["password_hash"],
        "secure-password-123"
    )


# 2. Successful login and dashboard access
def test_login_and_dashboard(client):
    register_user(client)

    response = login_user(
        client,
        "testuser",
        "secure-password-123"
    )

    assert response.status_code == 302
    assert client.get("/dashboard").status_code == 200


# 3. Normal users cannot access admin dashboard
def test_normal_user_cannot_access_admin(client):
    register_user(client)

    login_user(
        client,
        "testuser",
        "secure-password-123"
    )

    assert client.get("/admin").status_code == 403


# 4. Admin can access admin dashboard
def test_admin_can_access_admin_dashboard(client):
    response = login_user(
        client,
        "testadmin",
        "test-admin-password"
    )

    assert response.status_code == 302
    assert client.get("/admin").status_code == 200


# 5. Logout clears the session
def test_logout_clears_session(client):
    register_user(client)

    login_user(
        client,
        "testuser",
        "secure-password-123"
    )

    token = get_csrf_token(client, "/dashboard")

    response = client.post("/logout", data={
        "csrf_token": token
    })

    assert response.status_code == 302
    assert client.get("/dashboard").status_code == 302


# 6. Missing CSRF token is rejected during registration
def test_csrf_protection_rejects_missing_token(client):
    response = client.post("/register", data={
        "username": "attacker",
        "password": "secure-password-123"
    })

    assert response.status_code == 400


# 7. Short passwords are rejected
def test_short_password_rejected(client):
    response = register_user(
        client,
        "shortuser",
        "weak123"
    )

    assert response.status_code == 400


# 8. Duplicate usernames are rejected
def test_duplicate_username_rejected(client):
    first = register_user(client)

    assert first.status_code == 302

    second = register_user(client)

    assert second.status_code == 409


# 9. Invalid login credentials are rejected
def test_invalid_login_rejected(client):
    register_user(client)

    response = login_user(
        client,
        "testuser",
        "incorrect-password"
    )

    assert response.status_code == 401


# 10. Normal registration cannot create an admin
def test_registration_assigns_user_role(client):
    register_user(client)

    with auth.get_db() as conn:
        user = conn.execute(
            "SELECT role FROM users WHERE username = ?",
            ("testuser",)
        ).fetchone()

    assert user["role"] == "user"


# 11. Logout without CSRF token is rejected
def test_logout_rejects_missing_csrf_token(client):
    register_user(client)

    login_user(
        client,
        "testuser",
        "secure-password-123"
    )

    response = client.post("/logout")

    assert response.status_code == 400
