from flask import Flask
import os

# Initialization - application instance
application = Flask(__name__)
application.secret_key = os.urandom(33)  # For CSRF token

from app import routes