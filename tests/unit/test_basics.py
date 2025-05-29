import json
from unittest.mock import mock_open, patch

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
    assert len(result) == 2


def test_loadCompetitions(test_data):
    fake_json = json.dumps({"competitions": test_data["competitions"]})

    with patch("builtins.open", mock_open(read_data=fake_json)):
        result = loadCompetitions()

    assert isinstance(result, list)
    assert result[0]["name"] == "The Big Chest Challenge"
    assert result[1]["date"] == "2025-11-15"
    assert result[1]["numberOfPlaces"] == "200"
    assert len(result) == 2
