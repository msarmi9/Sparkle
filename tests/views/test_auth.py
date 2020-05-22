"""
Tests user registration and login/logout.
"""
import pytest

from app import db
from app.models.persons import User
from tests.utils import captured_templates


class TestRegisterFlow:
    """Test registration flow for new and existing users."""

    def test_register_view(self, app, client):
        """Register view is rendered when requesting ``/register`` endpoint."""
        with captured_templates(app) as templates:
            response = client.get("/register")
            template, context = templates[0]
            assert response.status_code == 200
            assert template.name == "auth/register.html"

    def test_register_new_user(self, app, client, user_data):
        """New users are registered in the database and redirected to login page."""
        with captured_templates(app) as templates:
            response = client.post("/register", data=user_data, follow_redirects=True)
            template, context = templates[0]
            assert response.status_code == 200
            assert User.query.filter_by(username=user_data["username"]).count() == 1
            assert template.name == "auth/login.html"

    def test_error_on_existing_username_or_email(self, client, user_data, init_user):
        """Error thrown when trying to register with an existing username or email."""
        response = client.post("/register", data=user_data, follow_redirects=True)
        assert response.status_code == 401
        assert b"Error!" in response.data

    def test_forgot_password(self, app, client):
        """Forgot password view is rendered."""
        with captured_templates(app) as templates:
            response = client.get("/forgot_password")
            template, context = templates[0]
            assert response.status_code == 200
            assert template.name == "auth/forgot_password.html"


class TestLoginLogoutFlow:
    """Test login/logout flow for new and existing users."""

    def test_login_view(self, app, client):
        """Login view is rendered when requesting ``/login`` endpoint."""
        with captured_templates(app) as templates:
            response = client.get("/login")
            template, context = templates[0]
            assert response.status_code == 200
            assert template.name == "auth/login.html"

    def test_login_existing_user(self, app, client, user_data, init_user):
        """Existing users (doctors) are redirected to ``patients`` page after login."""
        data = {"username": user_data["username"], "password": user_data["password"]}
        with captured_templates(app) as templates:
            response = client.post("/login", data=data, follow_redirects=True)
            template, context = templates[0]
            assert response.status_code == 200
            assert template.name == "patients/patients.html"

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

    def test_logout_user(self, app, client, login_user):
        """Logged in users are logged out and redirected to home page."""
        with captured_templates(app) as templates:
            response = client.get("/logout", follow_redirects=True)
            template, context = templates[0]
            assert response.status_code == 200
            assert template.name == "home/splash.html"
