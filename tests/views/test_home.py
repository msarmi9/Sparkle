"""
Tests home and about pages render correctly.
"""


def test_index(client):
    """Index (home) page renders."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Lift off to better health outcomes" in response.data


def test_about(client):
    """About page renders."""
    response = client.get("/about")
    assert response.status_code == 200
    assert b"About Sparkle.ai" in response.data
