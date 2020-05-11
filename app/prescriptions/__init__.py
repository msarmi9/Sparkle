from flask import Blueprint

bp = Blueprint("prescriptions", __name__)

from . import views
