def test_cannot_use_more_points_than_available(client):
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Pelpass Festival", "club": "Iron Temple", "places": "2"},
        follow_redirects=True,
    )

    body = response.data.decode("utf-8")
    assert response.status_code == 200
    assert "You do not have enough points to book 2 places." in body

    # Et le nombre de points du club n'a PAS changé
    from server import clubs

    iron = next(c for c in clubs if c["name"] == "Iron Temple")
    assert int(iron["points"]) == 4
