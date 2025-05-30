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


def test_purchase_places_route(client, test_data, patch_server_data):
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
    assert b"Great-booking complete!" in response.data
    assert bytes(club["name"], "utf-8") in response.data
    assert bytes(competition["name"], "utf-8") in response.data
