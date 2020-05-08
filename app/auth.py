from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import login_user
from flask_login import logout_user

from app import db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.persons import User


bp = Blueprint("auth", __name__)


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Registers a new doctor (user) from form data."""
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        firstname = registration_form.firstname.data
        lastname = registration_form.lastname.data
        username = registration_form.username.data
        password = registration_form.password.data
        email = registration_form.email.data

        user_count = (
            User.query.filter_by(username=username).count()
            + User.query.filter_by(email=email).count()
        )

        if user_count > 0:
            return "<h1>Error - Existing user : " + username + " OR " + email + "</h1>"
        else:
            user = User(firstname, lastname, username, email, password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for(".login"))
    return render_template("register.html", form=registration_form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Log in a returning User (doctor)."""
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        # Look for it in the database.
        user = User.query.filter_by(username=username).first()

        # Login and validate the user; take them to dashboard page.
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for("dashboard.dashboard"))
    return render_template("login.html", form=login_form)


@bp.route("/logout")
def logout():
    """Log out a User."""
    logout_user()
    return redirect(url_for("index"))
