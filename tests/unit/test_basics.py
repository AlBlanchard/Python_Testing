import json
from unittest.mock import mock_open, patch
from server import find_club_by_email
from datetime import datetime, timedelta
from tests.utils import get_tomorrow

from server import (
    loadClubs,
    loadCompetitions,
    find_club_by_name,
    find_competition_by_name,
    is_competition_in_past,
)


def test_loadClubs(test_data):
    fake_json = json.dumps({"clubs": test_data["clubs"]})

    # Parch open pour retourner le JSON factice
    with patch("builtins.open", mock_open(read_data=fake_json)):
        result = loadClubs()

    # Vérifie que le résultat est une liste de clubs
    assert isinstance(result, list)
    assert result[0]["name"] == "Big Chest"
    assert result[1]["email"] == "louis@armstrong.com"
    assert result[1]["points"] == "40"


def test_loadCompetitions(test_data):
    fake_json = json.dumps({"competitions": test_data["competitions"]})

    with patch("builtins.open", mock_open(read_data=fake_json)):
        result = loadCompetitions()

    assert isinstance(result, list)
    assert result[0]["name"] == "The Big Chest Challenge"
    assert result[1]["numberOfPlaces"] == "200"


def test_find_club_by_email_found(test_data):
    clubs = test_data["clubs"]

    result = find_club_by_email("tim@bigchest.com", clubs)
    assert result["name"] == "Big Chest"


def test_find_club_by_email_not_found(test_data):
    clubs = test_data["clubs"]

    result = find_club_by_email("djo@biscoto.fr", clubs)
    assert result is None


def test_find_club_by_name_found(test_data):
    clubs = test_data["clubs"]

    result = find_club_by_name("Big Chest", clubs)
    assert result["email"] == "tim@bigchest.com"


def test_find_club_by_name_not_found(test_data):
    clubs = test_data["clubs"]

    result = find_club_by_name("Djo Biscoto", clubs)
    assert result is None


def test_find_competition_by_name_found(test_data):
    formatted_tomorrow = get_tomorrow()

    competitions = test_data["competitions"]

    result = find_competition_by_name("Arm Strong Showdown", competitions)
    assert result["date"] == f"{formatted_tomorrow}"


def test_find_competition_by_name_not_found(test_data):
    competitions = test_data["competitions"]

    result = find_competition_by_name("Man of Steel Challenge", competitions)
    assert result is None


def test_is_competition_in_past_true():
    past_competition = {
        "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    }
    assert is_competition_in_past(past_competition) is True


def test_is_competition_in_past_false():
    future_competition = {
        "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    }
    assert is_competition_in_past(future_competition) is False
