"""
Tests views for adding new patient prescriptions.
"""
from app.utils import adherence
from tests.utils import captured_templates


class TestPrescriptionView:
    """Tests for prescription views and endpoints."""

    def test_rx_view_requires_login(self, client, init_patient):
        """Non-logged in users (doctors) cannot access add prescription view."""
        response = client.get("/patients/1/new-prescription")
        assert response.status_code == 401

    def test_add_rx_view(self, app, client, login_user, patient, init_patient):
        """Add prescription view renders for logged in users."""
        with captured_templates(app) as templates:
            response = client.get("/patients/1/new-prescription")
            template, context = templates[0]
            assert response.status_code == 200
            assert context["patient"] == patient
            assert template.name == "prescriptions/add_prescription.html"

    def test_add_rx(self, app, client, login_user, rx_data, init_patient):
        """New rxs are added to the db and users are redirected to the patient view."""
        endpoint = "/patients/1/new-prescription"
        rx_data["dosage"] = list(adherence.DOSAGE_TO_FREQ.keys())[0]
        with captured_templates(app) as templates:
            response = client.post(endpoint, data=rx_data, follow_redirects=True)
            template, context = templates[0]
            patient = context["patient"]
            assert response.status_code == 200
            assert patient.id == 1
            assert len(patient.prescriptions) == 1
            assert patient.prescriptions[0].drug == rx_data["drug"]
            assert template.name == "patients/patient_profile.html"
