"""
Tests for adding Users (doctors) and Patients to a database.
"""
import pytest

from app import db
from app.models.persons import Patient
from app.models.persons import User


class TestUser:
    """Tests ``models.persons.User`` class."""

    def test_add_user(self, client, user, init_user):
        """Users are added to the database."""
        assert User.query.filter_by(username=user.username).count() == 1

    def test_set_password(self, client, user_data, user, init_user):
        """User passwords are hashed, then stored in the database."""
        user.set_password(user_data["password"])
        hash_val = User.query.filter_by(username=user.username).first().password_hash
        assert hash_val != user_data["password"]

    def test_check_password(self, user, user_data):
        """Unhashed user password matches original password."""
        assert user.check_password(user_data["password"])


class TestPatient:
    """Tests ``models.persons.Patient`` class."""

    patient = Patient("Cathy", "Earnshaw", email="", age=24, weight=123)

    def test_all_intakes(self):
        """List of prescribed intakes for a patient is returned."""
        assert len(self.patient.all_intakes()) == 0

    def test_adherence_stats(self):
        """Dict of adherence statistics for a patient is returned."""
        assert type(self.patient.adherence_stats()) is dict

    def test_frac_adhering_prescriptions(self):
        """Dict of prescriptions a patient is adhering to is returned."""
        assert type(self.patient.frac_adhering_prescriptions()) is dict

    def test_is_adherent(self):
        """Patients with no prescriptions are adherent by default."""
        assert self.patient.is_adherent()
