import json
from tests.utils import login_dashboard


def test_logout_redirects(client):
    response = client.get("/logout")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


# Tests pour se connecter et voir le tableau de bord
def test_user_can_log_in_and_see_dashboard(client, test_data):
    email = test_data["clubs"][0]["email"]

    response = login_dashboard(client, email, test_data)

    assert response.status_code == 200
    assert f"Welcome, {email}".encode() in response.data
    assert bytes(email, "utf-8") in response.data
    assert bytes(test_data["competitions"][0]["name"], "utf-8") in response.data


def test_unknown_user_cannot_log_in(client, test_data):
    email = "test@unknown.com"
    response = login_dashboard(client, email, test_data)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_none_user_cannot_log_in(client, test_data):
    email = None
    response = login_dashboard(client, email, test_data)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


# Tests pour la route /showSummary
def test_user_can_access_booking_page(client, test_data):
    email = test_data["clubs"][0]["email"]
    competition_name = test_data["competitions"][0]["name"]
    club_name = test_data["clubs"][0]["name"]

    client.post("/showSummary", data={"email": email})
    response = client.get(f"/book/{competition_name}/{club_name}")

    assert response.status_code == 200
    assert b"Booking for" in response.data
    assert bytes(club_name, "utf-8") in response.data
    assert bytes(competition_name, "utf-8") in response.data


def test_user_cannot_access_unknow_competition(client, test_data):
    competition_name = "Unknown Competition"
    club_name = test_data["clubs"][0]["name"]
    email = test_data["clubs"][0]["email"]

    login_dashboard(client, email, test_data, follow_redirects=True)
    response = client.get(f"/book/{competition_name}/{club_name}")

    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data


# Tests pour la route /book/<competition>/<club>
def test_booking_future_competition_functional(client, test_data):
    email = test_data["clubs"][0]["email"]
    club_name = test_data["clubs"][0]["name"]
    competition_name = test_data["competitions"][0]["name"]

    login_dashboard(client, email, test_data, follow_redirects=True)
    response = client.get(
        f"/book/{competition_name}/{club_name}", follow_redirects=True
    )

    assert response.status_code == 200
    assert f"Booking for {competition_name}".encode() in response.data


def test_booking_past_competition_functional(client, test_data):
    email = test_data["clubs"][0]["email"]
    club_name = test_data["clubs"][0]["name"]
    competition_name = test_data["competitions"][2]["name"]

    login_dashboard(client, email, test_data, follow_redirects=True)
    response = client.get(
        f"/book/{competition_name}/{club_name}", follow_redirects=True
    )

    assert response.status_code == 200
    assert b"You cannot book places for a past competition." in response.data


def test_booking_unknown_competition_and_club(client, test_data):
    email = test_data["clubs"][0]["email"]

    # Simule la connexion d'un utilisateur valide
    login_dashboard(client, email, test_data, follow_redirects=True)

    response = client.get("/book/UnknownCompetition/UnknownClub", follow_redirects=True)

    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data


# Tests pour la route /purchasePlaces
def test_booking_past_competition_purchase_places(client, test_data):
    email = test_data["clubs"][0]["email"]
    club_name = test_data["clubs"][0]["name"]
    competition_name = test_data["competitions"][2]["name"]  # compétition passée
    places_required = 1

    login_dashboard(client, email, test_data, follow_redirects=True)

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": str(places_required),
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"You cannot book places for a past competition." in response.data


def test_booking_too_many_places_functional(client, test_data):
    email = test_data["clubs"][0]["email"]
    club_name = test_data["clubs"][0]["name"]
    competition_name = test_data["competitions"][0]["name"]
    places_required = 100

    login_dashboard(client, email, test_data, follow_redirects=True)
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": str(places_required),
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"You cannot book more than" in response.data


def test_booking_enough_places_functional(client, test_data):
    email = test_data["clubs"][0]["email"]
    club_name = test_data["clubs"][0]["name"]
    competition_name = test_data["competitions"][1]["name"]
    places_required = 5

    login_dashboard(client, email, test_data, follow_redirects=True)
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": str(places_required),
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert bytes(club_name, "utf-8") in response.data
    assert bytes(competition_name, "utf-8") in response.data


def test_booking_invalid_places_entry_functional(client, test_data):
    email = test_data["clubs"][0]["email"]
    club_name = test_data["clubs"][0]["name"]
    competition_name = test_data["competitions"][1]["name"]
    places_required = "invalid"

    login_dashboard(client, email, test_data, follow_redirects=True)
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": places_required,
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid number of places entered." in response.data
    assert bytes(club_name, "utf-8") in response.data
    assert bytes(competition_name, "utf-8") in response.data


def test_booking_above_limit_places_functional(client, test_data):
    email = test_data["clubs"][1]["email"]
    club_name = test_data["clubs"][1]["name"]
    competition_name = test_data["competitions"][1]["name"]
    places_required = 13

    login_dashboard(client, email, test_data, follow_redirects=True)
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": str(places_required),
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"You cannot book more than 12 places at once." in response.data
    assert bytes(club_name, "utf-8") in response.data
    assert bytes(competition_name, "utf-8") in response.data


def test_booking_under_limit_places_functional(client, test_data):
    email = test_data["clubs"][1]["email"]
    club_name = test_data["clubs"][1]["name"]
    competition_name = test_data["competitions"][1]["name"]
    places_required = 12

    login_dashboard(client, email, test_data, follow_redirects=True)
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": str(places_required),
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert bytes(club_name, "utf-8") in response.data
    assert bytes(competition_name, "utf-8") in response.data


def test_not_enough_points_to_purchase_functional(client, test_data):
    email = test_data["clubs"][1]["email"]
    club_name = test_data["clubs"][0]["name"]
    competition_name = test_data["competitions"][1]["name"]
    places_required = 11

    login_dashboard(client, email, test_data, follow_redirects=True)
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": str(places_required),
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert (
        b"You do not have enough points to book this number of places." in response.data
    )
    assert bytes(club_name, "utf-8") in response.data
    assert bytes(competition_name, "utf-8") in response.data


def test_enough_points_to_purchase_functional(client, test_data):
    email = test_data["clubs"][1]["email"]
    club_name = test_data["clubs"][1]["name"]
    competition_name = test_data["competitions"][1]["name"]
    places_required = 5

    login_dashboard(client, email, test_data, follow_redirects=True)
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": str(places_required),
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert bytes(club_name, "utf-8") in response.data
    assert bytes(competition_name, "utf-8") in response.data


def test_club_points_updated_after_purchase_functional(
    client, test_data, isolated_test_db
):
    competition = test_data["competitions"][1]
    club = test_data["clubs"][1]
    email = club["email"]
    places_required = 5

    initial_points = int(test_data["clubs"][1]["points"])

    login_dashboard(client, email, test_data, follow_redirects=True)
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "places": str(places_required),
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert bytes(club["name"], "utf-8") in response.data
    assert bytes(competition["name"], "utf-8") in response.data

    clubs_db_file, competitions_db_file = isolated_test_db

    with open(clubs_db_file, "r", encoding="utf-8") as f:
        clubs_data = json.load(f)["clubs"]

    updated_club = next((c for c in clubs_data if c["name"] == club["name"]), None)
    assert updated_club is not None
    assert int(updated_club["points"]) == initial_points - places_required


def test_competition_places_updated_after_purchase_functional(
    client, test_data, isolated_test_db
):
    competition = test_data["competitions"][1]
    club = test_data["clubs"][1]
    email = club["email"]
    places_required = 5

    initial_places = int(competition["numberOfPlaces"])

    login_dashboard(client, email, test_data, follow_redirects=True)
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "places": str(places_required),
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert bytes(club["name"], "utf-8") in response.data
    assert bytes(competition["name"], "utf-8") in response.data

    clubs_db_file, competitions_db_file = isolated_test_db

    with open(competitions_db_file, "r", encoding="utf-8") as f:
        competitions_data = json.load(f)["competitions"]

    updated_competition = next(
        (c for c in competitions_data if c["name"] == competition["name"]), None
    )
    assert updated_competition is not None
    expected_places = initial_places - places_required
    assert int(updated_competition["numberOfPlaces"]) == expected_places


def test_functional_points_board_logged_in(client, test_data):
    email = test_data["clubs"][0]["email"]
    club_name = test_data["clubs"][0]["name"]

    client.post("/showSummary", data={"email": email}, follow_redirects=True)

    response = client.get("/points", follow_redirects=True)

    assert response.status_code == 200
    assert b"Points Board" in response.data
    assert bytes(club_name, "utf-8") in response.data
    assert b"Back to the board" in response.data


def test_functional_points_board_anonymous(client):
    response = client.get("/points", follow_redirects=True)
    assert response.status_code == 200
    assert b"Points Board" in response.data
    assert b"Back to the login" in response.data
