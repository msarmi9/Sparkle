from flask import Blueprint

bp = Blueprint("prescriptions", __name__, template_folder="templates")

from . import views
