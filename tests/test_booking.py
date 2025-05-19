import pytest
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_booking_past_competition(client):
    response = client.get("/book/Spring Festival/Iron Temple", follow_redirects=True)
    assert b"You cannot book places for a past competition." in response.data
