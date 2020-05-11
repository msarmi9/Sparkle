from flask import Blueprint

bp = Blueprint("home", __name__, template_folder="templates")

from . import views
