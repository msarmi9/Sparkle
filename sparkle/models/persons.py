"""
Classes to model users (doctors) and patients.
"""
from collections import defaultdict
from datetime import datetime

import numpy as np
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from sparkle import db
from sparkle import login_manager
from sparkle.models.medication import Prescription


class BasicInfo:
    """Base class for modeling users and patients."""

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), unique=False, nullable=False)
    lastname = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)


class User(db.Model, UserMixin, BasicInfo):
    """User model with functions to set and check password when logging in."""

    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    # One-to-many relationship
    patients = db.relationship("Patient", backref="user", lazy=True)

    def __init__(self, firstname, lastname, username, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Patient(db.Model, BasicInfo):
    """
    Defines a Patient, which has a foreign key pointed to User (doctor).
    """

    # Foreign key
    doctor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # One-to-many relationship
    prescriptions = db.relationship("Prescription", backref="patient", lazy=True)

    def __init__(self, firstname, lastname, email, age, weight):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.age = age
        self.weight = weight

    def all_intakes(self, start=None, end=None):
        """
        Return Intake objects associated with this Patient.
        start: datetime - optional start date for filtering
        end: datetime - optional end date for filtering

        TODO: Implement start, end filtering
        NOTE: There's probably a better way of doing this. Perhaps setting Patient
              as a foreign key in Intake?
        """
        all_intakes = []
        for rx in self.prescriptions:
            all_intakes += rx.intakes
        return all_intakes

    def adherence_stats(self, date=datetime.now()):
        """
        Return adherence statistics on a per-Prescription basis.
        return: dict - <prescription ID>: <details>
        Example:
        {
            1: {
                'frac_on_time': 0.932,
                'frac_required_intakes': 0.976
            },
            19: {
                'frac_on_time': 0.389,
                'frac_required_intakes': 1.0
            },
            ...
        }
        """
        stats = defaultdict(lambda: defaultdict(float))
        for rx in self.prescriptions:
            stats[rx.id]["frac_on_time"] = rx.frac_on_time(date=date)
            stats[rx.id]["frac_required_intakes"] = rx.frac_required_intakes(date=date)
        return dict(stats)

    def frac_adhering_prescriptions(
        self, on_time_threshold=0.9, required_intakes_threshold=0.9
    ):
        """
        Return fraction of prescriptions for this Patient that are deemed
        adherent.
        Adherence requires Intakes to be recorded on time and on track
        (i.e. medications aren't missed).

        on_time_threshold: float - fraction on time Intakes needed for
        this prescription to be deemed adherent
        required_intakes_threshold: float - fraction Intakes actually
        recorded, out of all prescribed Intakes since start date.
        """
        if len(self.prescriptions) == 0:
            return {}
        adherence = {}
        frac_on_time_by_rx = []
        frac_required_intakes_by_rx = []
        stats = self.adherence_stats()
        for rx_id, details in stats.items():
            frac_on_time_by_rx.append(details["frac_on_time"])
            frac_required_intakes_by_rx.append(details["frac_required_intakes"])

        adherence["on_time"] = np.sum(
            np.array(frac_on_time_by_rx) >= on_time_threshold
        ) / len(frac_on_time_by_rx)

        adherence["required_intakes"] = np.sum(
            np.array(frac_required_intakes_by_rx) >= required_intakes_threshold
        ) / len(frac_required_intakes_by_rx)
        return adherence

    def is_adherent(
        self, on_time_threshold=0.9, required_intakes_threshold=0.9, date=datetime.now()
    ):
        """
        Whether or not a patient is deemed adherent based on their
        prescription adherence.

        on_time_threshold: float - fraction on time Intakes needed for
        this prescription to be deemed adherent
        required_intakes_threshold: float - fraction Intakes actually
        recorded, out of all prescribed Intakes since start date.
        """
        if np.all([p.start_date > datetime.now() for p in self.prescriptions]):
            return True
        stats = self.adherence_stats(date=date)
        for rx_id, details in stats.items():
            if list(filter(lambda rx: rx.id == rx_id, self.prescriptions))[
                0
            ].start_date <= datetime.now() and (
                details["frac_on_time"] <= on_time_threshold
                or details["frac_required_intakes"] <= required_intakes_threshold
            ):
                return False
        return True


# Load user object from user ID stored in the current session
@login_manager.user_loader
def load_user(id):
    """
    This callback is used to reload the user object
    from the user ID stored in the session.
    """
    return User.query.get(int(id))
