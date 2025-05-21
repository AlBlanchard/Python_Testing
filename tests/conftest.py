import pytest
from server import app, loadClubs, loadCompetitions


# Autouse signifie que ce fixture sera utilisé automatiquement
# pour chaque test sans avoir besoin de l'inclure explicitement
@pytest.fixture(autouse=True)
def client():

    # Réinitialiser les données de test
    # en chargeant les clubs et compétitions
    import server

    server.clubs = loadClubs()
    server.competitions = loadCompetitions()

    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
