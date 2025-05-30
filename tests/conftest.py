import pytest
from server import app

from tests.utils import get_tomorrow, get_yesterday


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_data():
    formatted_tomorrow = get_tomorrow()
    formatted_yesterday = get_yesterday()

    clubs = [
        {"name": "Big Chest", "email": "tim@bigchest.com", "points": "10"},
        {"name": "Arm Strong", "email": "louis@armstrong.com", "points": "40"},
    ]

    competitions = [
        {
            "name": "The Big Chest Challenge",
            "date": f"{formatted_tomorrow}",
            "numberOfPlaces": "1",
        },
        {
            "name": "Arm Strong Showdown",
            "date": f"{formatted_tomorrow}",
            "numberOfPlaces": "200",
        },
        {
            "name": "Past Leg Day Madness",
            "date": f"{formatted_yesterday}",
            "numberOfPlaces": "200",
        },
    ]

    return {"clubs": clubs, "competitions": competitions}
