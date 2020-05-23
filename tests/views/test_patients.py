"""
Tests patients views and patient registration flow.
"""
from datetime import datetime

import pytest
from dateutil.relativedelta import relativedelta

from app import db
from tests.utils import captured_templates


views = [
    "/patients",
    "/patients_unprescribed",
    "/patients_deviating",
    "/patients_ontrack",
]


class TestPatientViews:
    """Tests for views for all, unprescribed, deviating, and ontrack patients."""

    @pytest.mark.parametrize("view", views)
    def test_patient_view_requires_login(self, client, view):
        """All patient views require users (doctors) to be logged in."""
        response = client.get(view)
        assert response.status_code == 401

    @pytest.mark.parametrize("view", views)
    def test_empty_view_if_no_patients(self, app, client, login_user, view):
        """Patient view is empty if there are no patients."""
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

    def test_patient_profile(self, app, client, login_user, init_perfect_patient):
        """Detail view for single patient view is rendered."""
        with captured_templates(app) as templates:
            response = client.get("/patients/1")
            template, context = templates[0]
            assert response.status_code == 200
            assert context["patient"].id == 1
            assert context["prescriptions"][0].drug == "Vitamin C++"
            assert template.name == "patients/patient_profile.html"


class TestAddPatient:
    """Tests for adding new patients to the database."""

    def test_add_patient_view(self, app, client, login_user):
        """View for adding new patients renders when requesting ``/new-patient``."""
        with captured_templates(app) as templates:
            response = client.get("/new-patient")
            template, context = templates[0]
            assert response.status_code == 200
            assert template.name == "patients/add_patient.html"

    def test_add_new_patient(self, app, client, login_user, patient_data):
        """New patient is added to the db."""
        with captured_templates(app) as templates:
            r = client.post("/new-patient", data=patient_data, follow_redirects=True)
            template, context = templates[0]
            patients = context["current_user"].patients
            assert r.status_code == 200
            assert len(patients) == 1
            assert patients[0].firstname == patient_data["firstname"]
            assert template.name == "patients/patients.html"
