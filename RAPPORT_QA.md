# Rapport QA 

---

## IMPROVEMENT 1 : Ajout des tests de base

Branche : improvement/base-tests

* **Organisation** :

  * `tests/unit/` : tests unitaires
  * `tests/integration/` : tests d'intégration
  * `conftest.py` : fixtures de données communes
  * `pytest.ini` : racine du projet configurée pour pytest

### Tests réalisés

#### Unitaires

Via le fichier /tests/unit/test_basics.py

* `loadClubs()` : chargement JSON avec mock
* `loadCompetitions()` : idem

#### Intégration

Via le fichier /tests/integration/test_routes_integration.py

* `/showSummary` : connexion utilisateur valide/invalide
* `/book/<competition>/<club>` : accès réservation + message d'erreur
* `/purchasePlaces` : réservation normale, trop de places, >12 places

#### Fonctionnels

Via le fichier /tests/functional/test_routes_functional.py

* `/logout` : redirection vers accueil

### État actuel

* Tous les tests passent
* Bonne couverture sur les routes critiques

---