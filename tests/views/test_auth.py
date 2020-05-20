"""
Tests user registration and login/logout.
"""
import pytest

from app import db
from app.models.persons import User


@pytest.fixture
def login_user(client, user_data, init_user):
    """Return the response from logging in an existing user."""
    data = {"username": user_data["username"], "password": user_data["password"]}
    response = client.post("/login", data=data, follow_redirects=True)
    return response


class TestRegisterFlow:
    """Test registration flow for new and existing users."""

    def test_register_view(self, client):
        """Register view is rendered when requesting ``/register`` endpoint."""
        response = client.get("/register")
        assert response.status_code == 200
        assert b"Register" in response.data

    def test_register_new_user(self, client, user_data):
        """New users are registered in the database and redirected to login page."""
        response = client.post("/register", data=user_data, follow_redirects=True)
        assert User.query.filter_by(username=user_data["username"]).count() == 1
        assert b"Login" in response.data

    def test_error_on_existing_username_or_email(self, client, user_data, init_user):
        """Error thrown when trying to register with an existing username or email."""
        response = client.post("/register", data=user_data, follow_redirects=True)
        assert b"Error" in response.data

    def test_forgot_password(self, client):
        """Forgot password view is rendered."""
        response = client.get("/forgot_password")
        assert b"Forgot Password" in response.data


class TestLoginLogoutFlow:
    """Test login/logout flow for new and existing users."""

    def test_login_view(self, client):
        """Login view is rendered when requesting ``/login`` endpoint."""
        response = client.get("/login")
        assert response.status_code == 200
        assert b"Login" in response.data

    def test_login_existing_user(self, client, login_user):
        """Existing users (doctors) are redirected to ``patients`` page after login."""
        assert b"All Patients" in login_user.data

    def test_login_nonexistent_user(self, client):
        """Error thrown when trying to login with a username not in the database."""
        data = {"username": "bugs", "password": "bunny"}
        response = client.post("/login", data=data, follow_redirects=True)
        assert response.status_code == 401

    def test_login_incorrect_password(self, client, user_data, init_user):
        """Error thrown when trying to login with an incorrect password."""
        data = {"username": user_data["username"], "password": "wrong"}
        response = client.post("/login", data=data, follow_redirects=True)
        assert response.status_code == 401

    def test_logout_user(self, client, login_user):
        """Logged in users are logged out and redirected to home page."""
        response = client.get("/logout", follow_redirects=True)
        assert response.status_code == 200
        assert b"Sparkle Medication" in response.data
