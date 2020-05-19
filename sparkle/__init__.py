import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


# Initialization
# Create an application instance (an object of class Flask) which handles all requests.
application = Flask(__name__)
application.secret_key = os.urandom(33)  # For CSRF token
application.config.from_object("sparkle.config.Config")

# Create DB
db = SQLAlchemy(application)
db.create_all()
db.session.commit()

# login_manager needs to be initiated before running the app
login_manager = LoginManager()
login_manager.init_app(application)

from sparkle.api import mobile
from sparkle.views import auth
from sparkle.views import dashboard
from sparkle.views import home
from sparkle.views import patients
from sparkle.views import prescriptions

application.register_blueprint(mobile.bp)
application.register_blueprint(auth.bp)
application.register_blueprint(dashboard.bp)
application.register_blueprint(home.bp)
application.register_blueprint(patients.bp)
application.register_blueprint(prescriptions.bp)
