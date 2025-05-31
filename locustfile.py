from locust import HttpUser, task, between


class BookingUser(HttpUser):
    host = "http://127.0.0.1:5000"  # Ou le port utilisé par ton serveur Flask
    wait_time = between(1, 3)

    def on_start(self):
        self.email = "admin@irontemple.com"
        self.club_name = "Iron Temple"
        self.competition_name = "Not passed competition"

        response = self.client.post(
            "/showSummary",
            data={"email": self.email},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            name="/showSummary (login)",
        )

    @task
    def view_booking_page(self):
        self.client.get(f"/book/{self.competition_name}/{self.club_name}")

    @task
    def purchase_places(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "competition": self.competition_name,
                "club": self.club_name,
                "places": "1",
            },
        )

    @task
    def view_points_board(self):
        self.client.get("/pointsBoard")

    @task
    def logout(self):
        self.client.get("/logout")
