import os

from flask import Flask
from flask import render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import Config


application = Flask(__name__)
application.secret_key = os.urandom(33)  # For CSRF token
application.config.from_object(Config)

db = SQLAlchemy(application)
db.create_all()
db.session.commit()

login_manager = LoginManager()
login_manager.init_app(application)

from app import auth, dashboard, mobile

application.register_blueprint(auth.bp)
application.register_blueprint(dashboard.bp)
application.register_blueprint(mobile.bp)


@application.route("/")
@application.route("/home")
def index():
    """Render splash/home page."""
    return render_template("splash.html", message="Welcome to Sparkle!")
