from unittest.mock import patch
from datetime import datetime, timedelta


def login_dashboard(client, email, test_data, follow_redirects=False):
    """
    Helper pour simuler une connexion utilisateur.
    """
    with patch("server.clubs", test_data["clubs"]), patch(
        "server.competitions", test_data["competitions"]
    ):
        return client.post(
            "/showSummary", data={"email": email}, follow_redirects=follow_redirects
        )


def get_tomorrow():
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    formatted_tomorrow = tomorrow.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_tomorrow


def get_yesterday():
    now = datetime.now()
    yesterday = now - timedelta(days=1)

    formatted_yesterday = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_yesterday
