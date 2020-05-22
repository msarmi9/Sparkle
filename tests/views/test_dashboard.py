"""
Tests dashboard view displaying adherence statistics.
"""
from tests.utils import captured_templates


class TestDashboard:
    """Tests adherence dashboard renders for logged in users only."""

    def test_dashboard_requires_login(self, client):
        """Non-logged in users cannot view adherence dashboard."""
        response = client.get("/dashboard")
        assert response.status_code == 401

    def test_dashboard_view_no_rxs(self, app, client, login_user):
        """Dashboard view renders with no prescriptions."""
        with captured_templates(app) as templates:
            response = client.get("/dashboard")
            template, context = templates[0]
            assert response.status_code == 200
            assert type(context["adh_over_time"]) is str
            assert type(context["top_general_adh"]) is str
            assert type(context["top_ontime_adh"]) is str
            assert template.name == "dashboard/dashboard.html"

    def test_dashboard_view_rxs(self, app, client, login_user, init_patient_with_rxs):
        """Dashboard view renders with prescriptions."""
        with captured_templates(app) as templates:
            response = client.get("/dashboard")
            template, context = templates[0]
            assert response.status_code == 200
            assert template.name == "dashboard/dashboard.html"
