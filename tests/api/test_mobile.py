"""
Tests api for communicating with mobile clients.
"""
import json
from datetime import datetime

import pytest

from sparkle import db
from sparkle.models.medication import Prescription
from sparkle.models.persons import Patient
from sparkle.models.persons import User


@pytest.fixture
def init_db_patient():
    """Add a sample patient to the database."""
    doctor = User("Charlotte", "Bronte", "cbronte", "charlotte@me.com", "emily")
    patient = Patient("Jane", "Eyre", "jane@me.com", age=23, weight=123)
    patient.user = doctor
    patient.id = 0

    db.session.add(patient)
    db.session.commit()


@pytest.fixture
def sensor_json():
    """Return a json payload of watch sensor data sent by a mobile client."""
    test_file = "tests/data/2020-04-27_21_00_19_2.csv"
    with open(test_file, "r") as f:
        sensor_data = f.read()

    keys = ["id", "s3_url", "recording_data", "on_time", "timestamp"]
    values = ["-1", "s3", sensor_data, "0", "2999-12-31_11:59:59"]
    return dict(zip(keys, values))


@pytest.fixture
def login_json():
    """Return a json payload sent by a mobile client to login to the web api."""
    return {"patient_id": "0"}


def test_send_data(client, sensor_json):
    """API receives mobile json data and returns json response."""
    response = client.post("/send-data", json=sensor_json)
    pred_dict = json.loads(response.data)
    assert response.status_code == 200
    assert set(pred_dict.keys()) == {"pred_string", "pred_type", "pred"}


def test_mobile_login(client, init_db_patient, login_json):
    """Current day's medication schedule is returned when mobile clients log in."""
    response = client.post("mobile-login", json=login_json)
    assert response.status_code == 200
