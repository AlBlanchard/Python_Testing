import pytest
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_data():
    clubs = [
        {"name": "Big Chest", "email": "tim@bigchest.com", "points": "10"},
        {"name": "Arm Strong", "email": "louis@armstrong.com", "points": "40"},
    ]

    competitions = [
        {
            "name": "The Big Chest Challenge",
            "date": "2025-10-10",
            "numberOfPlaces": "100",
        },
        {
            "name": "Arm Strong Showdown",
            "date": "2025-11-15",
            "numberOfPlaces": "200",
        },
    ]

    return {"clubs": clubs, "competitions": competitions}
