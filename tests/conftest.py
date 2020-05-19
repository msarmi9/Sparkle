import pytest

from sparkle import create_app
from sparkle import db


@pytest.fixture(scope="module")
def app():
    """Configure a new instance of a Flask application for testing."""
    app = create_app()
    app.config.from_object("sparkle.config.TestConfig")
    with app.app_context():
        db.create_all()
        db.session.commit()
    yield app


@pytest.fixture(scope="module")
def client(app):
    """Return a test client for the app."""
    return app.test_client()
