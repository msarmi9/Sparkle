"""
Configure common fixtures to be shared across all test modules.
"""
import pytest

from app import create_app
from app import db
from app.models.persons import User


@pytest.fixture
def app():
    """Configure a fresh Flask app instance and db for testing."""
    app = create_app()
    app.config.from_object("app.config.TestConfig")
    with app.app_context():
        db.create_all()
        yield app


@pytest.fixture
def client(app):
    """Return a test client for the app."""
    return app.test_client()


@pytest.fixture
def user_data():
    """Return data for adding a sample user (doctor) to the database."""
    keys = ["firstname", "lastname", "username", "email", "password"]
    values = ["Anne", "Bronte", "annebronte", "anne@me.com", "emily"]
    user_data = dict(zip(keys, values))
    return user_data


@pytest.fixture
def user(user_data):
    """Return an instance of the ``models.persons.User`` class."""
    return User(**user_data)


@pytest.fixture
def init_user(user):
    """Add a sample user (doctor) to the database."""
    db.session.add(user)
    db.session.commit()
