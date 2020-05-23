"""
Tests for adding Users (doctors) and Patients to a database.
"""
import pytest

from app.models.persons import User


class TestUser:
    """Tests ``models.persons.User`` class."""

    def test_add_user(self, user, init_user):
        """Users are added to the database."""
        assert User.query.filter_by(username=user.username).count() == 1

    def test_set_password(self, user_data, user, init_user):
        """User passwords are hashed, then stored in the database."""
        user.set_password(user_data["password"])
        hash_val = User.query.filter_by(username=user.username).first().password_hash
        assert hash_val != user_data["password"]

    def test_check_password(self, user, user_data):
        """Unhashed user password matches original password."""
        assert user.check_password(user_data["password"])


class TestPatient:
    """Tests ``models.persons.Patient`` class."""

    def test_all_intakes_empty(self, patient):
        """List of intakes for a new patient is empty."""
        assert not patient.all_intakes()

    def test_all_intakes(self, patient, init_perfect_patient):
        """List of prescribed intakes for a patient is returned."""
        assert len(patient.all_intakes()) == 1

    def test_adherence_stats(self, patient, init_perfect_patient):
        """Dict of adherence statistics for a patient is returned."""
        stats = patient.adherence_stats()
        assert type(stats) is dict
        assert all(stats[id]["frac_on_time"] == 1.0 for id in stats.keys())
        assert all(stats[id]["frac_required_intakes"] == 1.0 for id in stats.keys())

    def test_frac_adhering_prescriptions(self, patient, init_perfect_patient):
        """Dict of prescriptions a patient is adhering to is returned."""
        adherence_dict = patient.frac_adhering_prescriptions()
        assert type(adherence_dict) is dict
        assert adherence_dict["on_time"] == 1.0
        assert adherence_dict["required_intakes"] == 1.0

    def test_is_adherent_by_default(self, patient):
        """Patients with no prescriptions are adherent by default."""
        assert patient.is_adherent()

    def test_is_adherent_perfect_patient(self, patient, init_perfect_patient):
        """Patients with perfect adherence records are marked as adherent."""
        assert patient.is_adherent()

    def test_is_adherent_deviating_patient(self, patient, init_patient_with_rxs):
        """Patients with prescriptions and no intakes are marked as non-adherent."""
        assert not patient.is_adherent()
