import json
import pytest
import server
from server import app

from tests.utils import get_tomorrow, get_yesterday


# Test data unique pour tous les tests (unitaires, intégration, fonctionnels)
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


# Fixture utilisée uniquement sur les tests unitaires / intégration (manuellement appelée)
@pytest.fixture
def patch_server_data(monkeypatch, test_data):
    monkeypatch.setattr(server, "clubs", test_data["clubs"])
    monkeypatch.setattr(server, "competitions", test_data["competitions"])


# Fixture automatique pour les tests fonctionnels (autouse)
@pytest.fixture(autouse=True)
def isolated_test_db(tmp_path, test_data, monkeypatch):
    """
    Avant chaque test :
     - on écrit test_data dans un JSON temporaire
     - on monkeypatch server.DB_FILE pour qu'il pointe dessus
     - on recharge server.data
    """
    clubs_data = test_data["clubs"]
    competitions_data = test_data["competitions"]

    clubs_db_file = tmp_path / "clubs.json"
    competitions_db_file = tmp_path / "competitions.json"

    clubs_db_file.write_text(
        json.dumps({"clubs": clubs_data}, indent=2)  # wrap dans un object, sinon plante
    )
    competitions_db_file.write_text(
        json.dumps({"competitions": competitions_data}, indent=2)
    )

    # Override le chemin dans le module server
    monkeypatch.setattr(server, "CLUBS_DB_FILE", str(clubs_db_file))
    monkeypatch.setattr(server, "COMPET_DB_FILE", str(competitions_db_file))

    # Recharge la variable globale data avant que Flask démarre
    server.clubs = server.loadClubs(filename=str(clubs_db_file))
    server.competitions = server.loadCompetitions(filename=str(competitions_db_file))

    return clubs_db_file, competitions_db_file


# Client Flask pour tous les tests
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
