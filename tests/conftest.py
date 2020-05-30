"""
Configure common fixtures to be shared across all test modules.
"""
from datetime import datetime

import pytest
from dateutil.relativedelta import relativedelta

from app import create_app
from app import db
from app.models.medication import Intake
from app.models.medication import Prescription
from app.models.persons import Patient
from app.models.persons import User


@pytest.fixture
def app():
    """Configure a new Flask app instance and db for each test."""
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
        yield app


@pytest.fixture
def client(app):
    """Return a test client for the app."""
    return app.test_client()


@pytest.fixture
def user_data():
    """Return data for creating a sample user (doctor)."""
    keys = ["firstname", "lastname", "username", "email", "password"]
    values = ["Charlotte", "Bronte", "cbronte", "cbronte@me.com", "emily"]
    user_data = dict(zip(keys, values))
    return user_data


@pytest.fixture
def user(user_data):
    """Return a User with the default user data."""
    return User(**user_data)


@pytest.fixture
def init_user(client, user):
    """Add a sample user (doctor) to the database."""
    db.session.add(user)
    db.session.commit()


@pytest.fixture
def login_user(client, user_data, init_user):
    """Login an existing user and return the response."""
    data = {"username": user_data["username"], "password": user_data["password"]}
    response = client.post("/login", data=data, follow_redirects=True)
    return response


@pytest.fixture
def patient_data(user):
    """Return data for creating a sample Patient associated with the default user."""
    keys = ["firstname", "lastname", "email", "age", "weight", "user"]
    values = ["Jane", "Eyre", "jane@me.com", "23", "123", user]
    return dict(zip(keys, values))


@pytest.fixture
def patient(patient_data):
    """Return a Patient belonging to the default user."""
    return Patient(**patient_data)


@pytest.fixture
def init_patient(client, patient):
    """Add a sample patient to the database belonging to the default user."""
    db.session.add(patient)
    db.session.commit()


@pytest.fixture
def init_patient_with_rxs(client, rx_past, rx_new, patient, init_patient):
    """Add sample patient with two prescriptions to the database."""
    rx_past.patient = patient
    rx_new.patient = patient
    db.session.add(rx_past)
    db.session.add(rx_new)
    db.session.commit()


@pytest.fixture
def init_perfect_patient(client, rx_current, intake, patient, init_patient):
    """Add an Patient with a 100% adherence record to the db."""
    rx_current.patient = patient
    intake.prescription = rx_current
    db.session.add(rx_current)
    db.session.commit()


@pytest.fixture
def intake():
    """Return an on-time Intake."""
    yesterday = datetime.now() - relativedelta(days=1)
    return Intake(timestamp=yesterday, on_time=True)


@pytest.fixture
def rx_past(rx_data):
    """Return a prescription with a long past start date (treatment has ended)."""
    start = datetime.fromisoformat("2000-01-01")
    rx_data["start_date"] = start
    rx_data["created"] = start
    return Prescription(**rx_data)


@pytest.fixture
def rx_current(rx_data):
    """Return a prescription with yesterday as the start date (treatment begins)."""
    yesterday = datetime.now() - relativedelta(days=1)
    rx_data["start_date"] = yesterday
    rx_data["created"] = yesterday
    return Prescription(**rx_data)


@pytest.fixture
def rx_new(rx_data):
    """Return a newly created prescription with today as the start date."""
    start = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    rx_data["start_date"] = start
    rx_data["created"] = start
    rx_data["last_refill_date"] = start
    rx_data["refills"] = 1
    return Prescription(**rx_data)


@pytest.fixture
def rx_data():
    """Return data for creating a new Prescription."""
    return {
        "drug": "Vitamin C++",
        "desc": "Improve hacking skills?",
        "strength": 30,
        "strength_unit": "mg",
        "quantity": 30,
        "drug_form": "tab",
        "amount": 1,
        "route": "oral",
        "freq": 1,
        "freq_repeat": 1,
        "freq_repeat_unit": "day",
        "duration": 1,
        "duration_unit": "month",
        "refills": 0,
        "time_of_day": "PM",
        "start_date": "01/01/2020",
        "created": "01/01/2020",
    }
