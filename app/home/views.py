from flask import render_template

from . import bp


@bp.route("/")
@bp.route("/home")
def index():
    """Render splash page."""
    return render_template("splash.html")


@bp.route("/about")
def about():
    """Render about page."""
    return render_template("about.html")
