from flask import Blueprint
from flask import render_template

bp = Blueprint("home", __name__)


@bp.route("/")
@bp.route("/home")
def index():
    """Render splash page."""
    return render_template("home/splash.html")


@bp.route("/about")
def about():
    """Render about page."""
    return render_template("home/about.html")
