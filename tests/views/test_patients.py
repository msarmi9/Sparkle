"""
Tests patients views and patient registration flow.
"""
from datetime import datetime

import pytest
from dateutil.relativedelta import relativedelta

from app import db
from app.models.medication import Intake
from tests.utils import captured_templates


views = [
    "/patients",
    "/patients_deviating",
    "/patients_unprescribed",
    "/patients_ontrack",
]


@pytest.fixture
def intake():
    """Return an ontime Intake."""
    yesterday = datetime.now() - relativedelta(days=1)
    return Intake(timestamp=yesterday, on_time=True)


@pytest.fixture
def init_perfect_patient(rx_current, intake, patient, init_patient):
    """Add an Patient with a 100% adherence record to the db."""
    rx_current.patient = patient
    intake.prescription = rx_current
    db.session.add(rx_current)
    db.session.commit()


class TestAllPatientViews:
    """Views for all, deviating, ontrack, and unprescribed patients are rendered."""

    @pytest.mark.parametrize("view", views)
    def test_patient_view_requires_login(self, client, view):
        """Users (doctors) cannot view patient data when not logged in."""
        response = client.get(view)
        assert response.status_code == 401

    @pytest.mark.parametrize("view", views)
    def test_empty_view_if_no_patients(self, app, client, login_user, view):
        """Empty patient view is rendered if there are no patients."""
        with captured_templates(app) as templates:
            response = client.get(view)
            template, context = templates[0]
            assert response.status_code == 200
            assert not context["patients"]
            assert template.name == f"patients{view}.html"

    def test_patients_unprescribed(self, app, client, login_user, init_patient):
        """Only unprescribed patients are shown (with null adherence)."""
        with captured_templates(app) as templates:
            response = client.get("/patients_unprescribed")
            template, context = templates[0]
            assert response.status_code == 200
            assert context["patients"]
            assert not context["rx_adherence"]
            assert template.name == "patients/patients_unprescribed.html"

    def test_patients_deviating(self, app, client, login_user, init_patient_with_rxs):
        """Only deviating patients are shown and are marked as non-adherent."""
        with captured_templates(app) as templates:
            response = client.get("/patients_deviating")
            template, context = templates[0]
            assert response.status_code == 200
            assert all(map(lambda p: not p.is_adherent(), context["patients"]))
            assert template.name == "patients/patients_deviating.html"

    def test_patients_adhering(self, app, client, login_user, init_perfect_patient):
        """Only adherent patients are shown and are marked as adherent."""
        with captured_templates(app) as templates:
            response = client.get("/patients_ontrack")
            template, context = templates[0]
            assert response.status_code == 200
            assert context["rx_adherence"] == 100
            assert all(map(lambda p: p.is_adherent(), context["patients"]))
            assert template.name == "patients/patients_ontrack.html"
