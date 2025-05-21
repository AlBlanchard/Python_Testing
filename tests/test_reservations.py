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


def test_points_reflected_after_booking(client):
    from server import clubs

    club_before = next(c for c in clubs if c["name"] == "Iron Temple")
    points_before = int(club_before["points"])
    places_to_book = 1
    cost = places_to_book * 3

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Pelpass Festival",
            "club": "Iron Temple",
            "places": str(places_to_book),
        },
        follow_redirects=True,
    )

    body = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Great-booking complete!" in body

    points_expected = points_before - cost
    assert f"Points available: {points_expected}" in body

    from server import clubs as clubs_after

    club_after = next(c for c in clubs_after if c["name"] == "Iron Temple")
    assert int(club_after["points"]) == points_expected
