from unittest.mock import patch
from tests.utils import login_dashboard


def test_show_summary_route_invalid_email(client, test_data):
    response = login_dashboard(
        client, "unknow@noexist.com", test_data, follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Sorry, we could not find your email address." in response.data
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
