def test_points_board_page(client):
    response = client.get("/points")
    body = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Iron Temple" in body
    from server import clubs

    iron = next(c for c in clubs if c["name"] == "Iron Temple")
    assert f"{iron['points']} points" in body
