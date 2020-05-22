"""
Marks dir as package and returns a configured instance of the Flask app.
"""
import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    """Create and configure an instance of the Flask app."""
    app = Flask(__name__)
    app.secret_key = os.urandom(33)  # For CSRF token
    app.config.from_object("app.config.Config")

    login_manager.init_app(app)
    db.init_app(app)

    from app.api import mobile
    from app.views import auth
    from app.views import dashboard
    from app.views import home
    from app.views import patients
    from app.views import prescriptions

    app.register_blueprint(mobile.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(patients.bp)
    app.register_blueprint(prescriptions.bp)

    with app.app_context():
        db.create_all()

    return app
