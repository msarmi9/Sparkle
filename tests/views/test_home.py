"""
Tests home and about pages render correctly.
"""
import pytest

from tests.utils import captured_templates


views = ["/", "/home"]


@pytest.mark.parametrize("view", views)
def test_index(app, client, view):
    """Index (home) page renders."""
    with captured_templates(app) as templates:
        response = client.get(view)
        template, context = templates[0]
        assert response.status_code == 200
        assert template.name == "home/splash.html"


def test_about(app, client):
    """About page renders."""
    with captured_templates(app) as templates:
        response = client.get("/about")
        template, context = templates[0]
        assert response.status_code == 200
        assert template.name == "home/about.html"
