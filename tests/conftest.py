import pytest

import sparkle


@pytest.fixture
def client():
    """Initialise flask application test client."""
    app = sparkle.create_app()
    app.config["TESTING"] = True
    app.config["DEBUG"] = True

    with app.test_client() as client:
        yield client
