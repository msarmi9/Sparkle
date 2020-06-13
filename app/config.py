import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base class for Flask configuration."""

    SECRET_KEY = os.urandom(33)
    SQLALCHEMY_DATABASE_URI = os.getenv("POSTGRES_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    """Configure Flask app for running tests."""

    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
