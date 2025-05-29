from unittest.mock import patch

from tests.utils import login_dashboard


def test_user_can_log_in_and_see_dashboard(client, test_data):
    email = test_data["clubs"][0]["email"]

    response = login_dashboard(client, email, test_data)

    assert response.status_code == 200
    assert f"Welcome, {email}".encode() in response.data
    assert bytes(email, "utf-8") in response.data
    assert bytes(test_data["competitions"][0]["name"], "utf-8") in response.data
