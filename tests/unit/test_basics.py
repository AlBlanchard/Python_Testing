import json
from unittest.mock import mock_open, patch
from server import find_club_by_email

from server import loadClubs, loadCompetitions


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
    assert result[1]["date"] == "2025-11-15"
    assert result[1]["numberOfPlaces"] == "200"


def test_find_club_by_email_found(test_data):
    clubs = test_data["clubs"]

    result = find_club_by_email("tim@bigchest.com", clubs)
    assert result["name"] == "Big Chest"


def test_find_club_by_email_not_found(test_data):
    clubs = test_data["clubs"]

    result = find_club_by_email("djo@biscoto.fr", clubs)
    assert result is None
