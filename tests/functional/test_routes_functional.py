from tests.utils import login_dashboard


def test_logout_redirects(client):
    response = client.get("/logout")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


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
