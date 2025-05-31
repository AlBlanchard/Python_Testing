import json
import server
from unittest.mock import patch
from tests.utils import login_dashboard


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data


def test_show_summary_route(client, test_data):
    email = test_data["clubs"][1]["email"]

    response = login_dashboard(client, email, test_data)

    assert response.status_code == 200
    assert f"Welcome, {email}".encode() in response.data


def test_show_summary_route_invalid_email(client, test_data):
    response = login_dashboard(
        client, "unknow@noexist.com", test_data, follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Sorry, we could not find your email address." in response.data
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data


# Bien garder patch_server_data dans les params des tests d'intégration
# C'est une fixture qui patch les données des clubs et compétitions
# Evite de se répéter avec les with patch dans chaque test
# C'est de la Fixture injection :)
def test_book_route_success(client, test_data, patch_server_data):
    competition = test_data["competitions"][0]["name"]
    club = test_data["clubs"][0]["name"]
    places = str(test_data["competitions"][0]["numberOfPlaces"])

    response = client.get(f"/book/{competition}/{club}")

    assert response.status_code == 200
    print(response.data)
    assert f"Booking for {competition}".encode() in response.data
    assert f"Places available: {places}".encode() in response.data
    assert bytes(competition, "utf-8") in response.data
    assert bytes(club, "utf-8") in response.data


def test_book_route_past_competition(client, test_data, patch_server_data):
    competition = test_data["competitions"][2]["name"]
    club = test_data["clubs"][0]["name"]

    response = client.get(f"/book/{competition}/{club}")

    assert response.status_code == 200
    assert b"You cannot book places for a past competition." in response.data


def test_book_route_failure(client, test_data, patch_server_data):
    club = test_data["clubs"][0]["name"]

    response = client.get(f"/book/Unknown Competition/{club}")

    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data


def test_enough_place_to_purchase(client, test_data, patch_server_data):
    competition = test_data["competitions"][1]
    club = test_data["clubs"][0]
    places_required = 5

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "places": str(places_required),
        },
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert bytes(club["name"], "utf-8") in response.data
    assert bytes(competition["name"], "utf-8") in response.data


def test_not_enough_place_to_purchase(client, test_data, patch_server_data):
    competition = test_data["competitions"][0]
    club = test_data["clubs"][0]
    places_required = 5

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "places": str(places_required),
        },
    )

    assert response.status_code == 200
    assert b"You cannot book more than" in response.data
    assert bytes(club["name"], "utf-8") in response.data
    assert bytes(competition["name"], "utf-8") in response.data


def test_invalid_place_to_purchase_entry(client, test_data, patch_server_data):
    competition = test_data["competitions"][0]
    club = test_data["clubs"][0]
    places_required = "invalid"

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "places": str(places_required),
        },
    )

    assert response.status_code == 200
    assert b"Invalid number of places entered." in response.data
    assert bytes(club["name"], "utf-8") in response.data
    assert bytes(competition["name"], "utf-8") in response.data


def test_above_limit_places_to_purchase(client, test_data, patch_server_data):
    competition = test_data["competitions"][1]
    club = test_data["clubs"][1]
    places_required = 13

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "places": str(places_required),
        },
    )

    assert response.status_code == 200
    assert b"You cannot book more than 12 places at once." in response.data
    assert bytes(club["name"], "utf-8") in response.data
    assert bytes(competition["name"], "utf-8") in response.data


def test_under_the_limit_places_to_purchase(client, test_data, patch_server_data):
    competition = test_data["competitions"][1]
    club = test_data["clubs"][1]
    places_required = 12

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "places": str(places_required),
        },
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert bytes(club["name"], "utf-8") in response.data
    assert bytes(competition["name"], "utf-8") in response.data


def test_not_enough_points_to_purchase(client, test_data, patch_server_data):
    competition = test_data["competitions"][1]
    club = test_data["clubs"][0]
    places_required = 11

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "places": str(places_required),
        },
    )

    assert response.status_code == 200
    assert (
        b"You do not have enough points to book this number of places." in response.data
    )
    assert bytes(club["name"], "utf-8") in response.data
    assert bytes(competition["name"], "utf-8") in response.data


def test_enough_points_to_purchase(client, test_data, patch_server_data):
    competition = test_data["competitions"][1]
    club = test_data["clubs"][1]
    places_required = 5

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "places": str(places_required),
        },
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert bytes(club["name"], "utf-8") in response.data
    assert bytes(competition["name"], "utf-8") in response.data


# Mettre tout de même isolated_test_db car pytest n'injecte pas le résultat directement
# Même si c'est en autouse
def test_club_points_update_after_purchase(client, test_data, isolated_test_db):
    competition = test_data["competitions"][1]
    club = test_data["clubs"][1]
    places_required = 5

    initial_points = int(test_data["clubs"][1]["points"])

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "places": places_required,
        },
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data

    # Récupère les fichiers temporaires de la fixture
    clubs_db_file, competitions_db_file = isolated_test_db

    with open(clubs_db_file, "r", encoding="utf-8") as f:
        clubs_data = json.load(f)["clubs"]

    # Relire depuis le fichier JSON réellement modifié
    updated_club = next((c for c in clubs_data if c["name"] == club["name"]), None)

    assert int(updated_club["points"]) == initial_points - places_required


def test_competition_places_update_after_purchase(client, test_data, isolated_test_db):
    competition = test_data["competitions"][1]
    club = test_data["clubs"][1]
    places_required = 5

    initial_places = int(competition["numberOfPlaces"])

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "places": str(places_required),
        },
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data

    clubs_db_file, competitions_db_file = isolated_test_db

    with open(competitions_db_file, "r", encoding="utf-8") as f:
        competitions_data = json.load(f)["competitions"]

    updated_competition = next(
        (c for c in competitions_data if c["name"] == competition["name"]), None
    )

    expected_places = initial_places - places_required
    assert int(updated_competition["numberOfPlaces"]) == expected_places


def test_points_board_logged_in(client, test_data, patch_server_data):
    email = test_data["clubs"][0]["email"]
    client.post("/showSummary", data={"email": email}, follow_redirects=True)

    response = client.get("/points")

    assert response.status_code == 200
    assert b"Points Board" in response.data
    assert bytes(test_data["clubs"][0]["name"], "utf-8") in response.data
    assert b"Back to the board" in response.data


def test_points_board_anonymous(client, patch_server_data):
    response = client.get("/points")

    assert response.status_code == 200
    assert b"Points Board" in response.data
    assert b"Back to the login" in response.data
