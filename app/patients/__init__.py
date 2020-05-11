from flask import Blueprint

bp = Blueprint("patients", __name__, template_folder="templates")

from . import views
