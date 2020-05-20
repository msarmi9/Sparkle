import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base class for Flask configuration."""

    SECRET_KEY = os.urandom(33)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "sparkle.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    """Configure Flask app for running tests."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
