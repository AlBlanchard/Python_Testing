from unittest.mock import patch


def login_dashboard(client, email, test_data, follow_redirects=False):
    """
    Envoie une requête POST vers /showSummary avec patch des données.

    :param client: le client de test Flask
    :param email: email du club à utiliser
    :param test_data: dictionnaire contenant clubs et competitions
    :param follow_redirects: booléen pour suivre les redirections
    :return: la réponse Flask
    """
    with patch("server.clubs", test_data["clubs"]), patch(
        "server.competitions", test_data["competitions"]
    ):
        return client.post(
            "/showSummary", data={"email": email}, follow_redirects=follow_redirects
        )
