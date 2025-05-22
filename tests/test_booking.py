def test_booking_past_competition(client):
    response = client.get("/book/Spring Festival/Iron Temple", follow_redirects=True)
    assert b"You cannot book places for a past competition." in response.data
