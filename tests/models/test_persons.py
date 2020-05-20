"""
Tests for adding Users (doctors) and Patients to a database.
"""
import pytest

from app import db
from app.models.persons import Patient
from app.models.persons import User


@pytest.mark.usefixtures("client")
class TestUser:
    """Tests ``models.persons.User`` class."""

    username = "emilybronte"
    password = "charlotte"
    user = User("Emily", "Bronte", email="", username=username, password=password)

    def test_add_user(self):
        """Users are added to the database."""
        db.session.add(self.user)
        db.session.commit()
        assert User.query.filter_by(username=self.username).count() == 1

    def test_set_password(self):
        """User passwords are hashed, then stored in the database."""
        self.user.set_password(self.password)
        hash_val = User.query.filter_by(username=self.username).first().password_hash
        assert hash_val != self.password

    def test_check_password(self):
        """Unhashed user password matches original password."""
        assert self.user.check_password(self.password)


@pytest.mark.usefixtures("client")
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
