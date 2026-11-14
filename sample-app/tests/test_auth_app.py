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


def register_user(client, username="testuser",
                  password="secure-password-123"):
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
        user["password_hash"], "secure-password-123"
    )


def test_login_and_dashboard(client):
    register_user(client)
    response = login_user(
        client, "testuser", "secure-password-123"
    )

    assert response.status_code == 302
    assert client.get("/dashboard").status_code == 200


def test_normal_user_cannot_access_admin(client):
    register_user(client)
    login_user(client, "testuser", "secure-password-123")

    assert client.get("/admin").status_code == 403


def test_admin_can_access_admin_dashboard(client):
    response = login_user(
        client, "testadmin", "test-admin-password"
    )

    assert response.status_code == 302
    assert client.get("/admin").status_code == 200


def test_logout_clears_session(client):
    register_user(client)
    login_user(client, "testuser", "secure-password-123")

    dashboard = client.get("/dashboard")
    match = re.search(
        r'name="csrf_token" value="([^"]+)"',
        dashboard.get_data(as_text=True)
    )
    assert match is not None

    response = client.post("/logout", data={
        "csrf_token": match.group(1)
    })

    assert response.status_code == 302
    assert client.get("/dashboard").status_code == 302


def test_csrf_protection_rejects_missing_token(client):
    response = client.post("/register", data={
        "username": "attacker",
        "password": "secure-password-123"
    })

    assert response.status_code == 400
