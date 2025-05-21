# tests/test_auth.py
import pytest
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_unknown_email_redirects_to_index(client):
    response = client.post(
        "/showSummary", data={"email": "no-such@club.com"}, follow_redirects=True
    )
    body = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Sorry, we could not find your email address." in body
    assert "<input" in body and 'name="email"' in body
