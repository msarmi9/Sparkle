"""
Public API for communicating with mobile clients.
"""
import json
from datetime import datetime

from flask import Blueprint
from flask import jsonify
from flask import request

from sparkle import db
from sparkle.adherence import adherence_model
from sparkle.models.medication import Intake
from sparkle.models.medication import Prescription
from sparkle.models.persons import Patient

bp = Blueprint("mobile", __name__)


@bp.route("/send-data", methods=["POST"])
def send_data():
    """Endpoint for receving json sensor data and returning json response."""
    content = request.get_json()

    # retrieving data for Intake table from json
    id = content["id"]  # request.headers["User-Agent"]
    s3_url = content["s3_url"]
    recording_data = content["recording_data"]
    timestamp = datetime.strptime(content["timestamp"], "%Y-%m-%d_%H:%M:%S")
    on_time = bool(int(content["on_time"]))
    print(f"data received: {recording_data}")

    # saving data to Intake table
    # rx = Prescription.query.filter_by(id=my_prescription_id).first()
    # note: this _requires_ there to be a prescription already in db!
    intake = Intake(
        s3_url=s3_url,
        recording_data=json.dumps(content),
        timestamp=timestamp,
        on_time=on_time,
        prescription_id=id,
    )
    db.session.add(intake)
    db.session.commit()

    model_pred_dict = adherence_model(recording_data)
    return jsonify(model_pred_dict)


@bp.route("/mobile-login", methods=["POST"])
def mobile_login():
    """Log in mobile users and return the current day's medication schedule."""
    # retrieving data from json request
    content = request.get_json()
    patient_id = content["patient_id"]

    # getting all prescriptions for all schedules
    rxs = Prescription.query.filter_by(patient_id=patient_id).all()
    schedules = [rx.generate_schedule() for rx in rxs]

    # getting only prescription for today (this can probably be optimized)
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    todays_schedule = [
        [metadata for date, metadata in day.items() if date == today]
        for schedule in schedules
        for day in schedule
    ]

    # getting name from Patient Table
    firstname = Patient.query.filter_by(id=patient_id).first().firstname

    # flattening and transforming datetime object to string
    todays_schedule = [
        metadata for rx in todays_schedule for metadata in rx if metadata
    ]
    for schedule in todays_schedule:
        schedule["timestamp"] = schedule["timestamp"].strftime("%Y-%m-%d_%H:%M:%S")
        schedule["firstname"] = firstname

    return jsonify(todays_schedule)
