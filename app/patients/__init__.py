from flask import Blueprint

bp = Blueprint("patients", __name__)

from . import views
