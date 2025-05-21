import pytest
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_points_board_page(client):
    response = client.get("/points")
    body = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Iron Temple" in body
    from server import clubs

    iron = next(c for c in clubs if c["name"] == "Iron Temple")
    assert f"{iron['points']} points" in body
