from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


# Initialization
# Create an application instance (an object of class Flask) which handles all requests.
application = Flask(__name__)
application.secret_key = os.urandom(33)  # For CSRF token
application.config.from_object(Config)

db = SQLAlchemy(application)
db.create_all()
db.session.commit()

# Added at the bottom to avoid circular dependencies. (Altough it violates PEP8 standards)
from app import classes
from app import routes
