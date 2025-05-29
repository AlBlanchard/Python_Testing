# Rapport QA 

---

## IMPROVEMENT 1 : Ajout des tests de base

**Branche** : `improvement/base-tests`

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

## FIX 1 : Invalid email fait planter l'app

**Branche** : `fix/show-summary-login-check`  

**Objectif** :  
Éviter les erreurs lors de la soumission d'un e-mail invalide et améliorer l'expérience utilisateur avec un message explicite et une redirection propre.

**Modifications** :
- Ajout d'un contrôle sur la validité de l'adresse e-mail saisie.
- Affichage d'un message Flash d'erreur si l'e-mail est introuvable.
- Redirection vers l'accueil ("/") dans ce cas.

### Tests réalisés

#### Intégration

`/tests/integration/test_show_summary.py`

- **Connexion avec e-mail valide**  
Affiche le tableau de bord avec le nom du club et les compétitions.

- **Connexion avec e-mail invalide**  
Affiche un message flash d'erreur + redirection vers la page d'accueil.

Utilisation du helper `login_dashboard()` pour éviter la duplication.

#### Fonctionnels

`/tests/functional/test_login_functional.py`

- **Connexion utilisateur valide**  
Vérifie la présence d'un message de bienvenue contenant l'adresse e-mail.  
Vérifie que les compétitions sont affichées correctement.

### État actuel

- Tous les tests passent  
- Comportement sécurisé en cas d'entrée incorrecte  
- Code prêt pour intégration continue

---