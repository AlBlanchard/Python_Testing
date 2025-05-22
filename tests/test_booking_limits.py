def test_cannot_book_more_than_12_places(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Hellfest Festival",
            "club": "Gym Bro",
            "places": "13",
        },
        follow_redirects=True,
    )

    body = response.data.decode("utf-8")
    assert response.status_code == 200
    assert "You cannot book more than 12 places at a time." in body

    # Vérification que rien n'a changé côté data
    from server import competitions as comps

    fall = next(c for c in comps if c["name"] == "Fall Classic")
    assert int(fall["numberOfPlaces"]) == 13  # la valeur initiale reste inchangée
