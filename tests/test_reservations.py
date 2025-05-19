import pytest
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_cannot_book_more_than_available(client):
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Pelpass Festival", "club": "Iron Temple", "places": "9"},
        follow_redirects=True,
    )

    body = response.data.decode("utf-8")
    assert "You cannot book more than 5 places for this competition." in body
