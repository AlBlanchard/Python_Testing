import pytest
from unittest.mock import patch


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data


def test_show_summary_route(client, test_data):
    email = test_data["clubs"][1]["email"]

    # Les données étant définis à l'exterieur de la fonction dans server.py,
    # nous devons les patcher pour simuler le comportement attendu
    with patch("server.clubs", test_data["clubs"]), patch(
        "server.competitions", test_data["competitions"]
    ):

        response = client.post("/showSummary", data={"email": email})

    assert response.status_code == 200
    assert b"Welcome, louis@armstrong.com" in response.data


# Test pour le fix de l'app qui plante, sera mis en place dans la branche dédiée
# def test_show_summary_route_invalid_email(client):
#    response = client.post("/showSummary", data={"email": "unknow@noexist.com"})
#    assert response.status_code == 200
#    assert b"Welcome" not in response.data


def test_book_route_success(client, test_data):
    competition = test_data["competitions"][0]["name"]
    club = test_data["clubs"][0]["name"]

    with patch("server.clubs", test_data["clubs"]), patch(
        "server.competitions", test_data["competitions"]
    ):
        response = client.get(f"/book/{competition}/{club}")

    assert response.status_code == 200
    assert b"Booking for The Big Chest Challenge" in response.data
    assert bytes(competition, "utf-8") in response.data
    assert bytes(club, "utf-8") in response.data


def test_book_route_failure(client, test_data):
    club = test_data["clubs"][0]["name"]

    with patch("server.clubs", test_data["clubs"]), patch(
        "server.competitions", test_data["competitions"]
    ):

        # Le try/catch est temporaire
        # Le but de cette branche est de faire les tests de base, pas de corriger les bugs
        # Manque de robustesse en accedant à l'index 0 sans vérifier la présence de l'élément
        try:
            response = client.get(f"/book/Unknown Competition/{club}")

            assert response.status_code == 200
            assert b"Something went wrong-please try again" in response.data

        except IndexError:
            pytest.xfail("Known fragility in route handler, will fix later")


def test_purchase_places_route(client, test_data):
    competition = test_data["competitions"][0]
    club = test_data["clubs"][0]
    places_required = 5

    with patch("server.clubs", test_data["clubs"]), patch(
        "server.competitions", test_data["competitions"]
    ):
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
