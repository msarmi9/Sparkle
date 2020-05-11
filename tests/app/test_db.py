from flask_testing import TestCase

from app import application
from app import db


class TestDB(TestCase):
    """Test sqlite database functionality."""

    def create_app(self):
        """Return a Flask instance."""
        return application

    def init_db(self):
        """Initialise sqlite session."""
        db.create_all()

    def close_db(self):
        """Close database session and remove tables."""
        db.session.remove()
        db.drop_all()
