# Rapport QA

---

## IMPROVEMENT 1 : Ajout des tests de base

**Branche** : `improvement/base-tests`

**Organisation** :

- `tests/unit/` : tests unitaires
- `tests/integration/` : tests d'intégration
- `tests/functional/` : tests fonctionnels
- `conftest.py` : fixtures de données communes
- `pytest.ini` : racine du projet configurée pour pytest

### Tests réalisés

#### Unitaires

Fichier : `tests/unit/test_basics.py`

- `loadClubs()` : chargement JSON avec mock
- `loadCompetitions()` : chargement JSON avec mock
- `find_club_by_email()`, `find_club_by_name()`, `find_competition_by_name()`
- `is_competition_in_past()`
- `is_not_enough_places_available()`

#### Intégration

Fichier : `tests/integration/test_routes_integration.py`

- `/` : accès à la page d'accueil
- `/showSummary` : connexion utilisateur valide et invalide
- `/book/<competition>/<club>` :
  - accès normal à la page de réservation
  - accès refusé pour compétition passée
  - accès refusé pour club ou compétition inexistants
- `/purchasePlaces` :
  - réservation normale
  - réservation avec trop de places disponibles
  - réservation avec entrée invalide (valeur négative, vide, non numérique)

#### Fonctionnels

Fichier : `tests/functional/test_routes_functional.py`

- Connexion et affichage du tableau de bord complet
- Déconnexion
- Tests des parcours utilisateurs complets de réservation
- Vérification du comportement lors d'entrées incorrectes

### Etat actuel

- Tous les tests passent
- Bonne couverture sur les routes critiques
- Comportement de l'application robuste et sécurisé

---

## FIX 1 : Invalid email fait planter l'application

**Branche** : `fix/show-summary-login-check`

**Objectif** :
Eviter les erreurs lors de la soumission d'un e-mail invalide et améliorer l'expérience utilisateur avec un message explicite et une redirection propre.

**Modifications** :

- Ajout d'un contrôle sur la validité de l'adresse e-mail saisie.
- Affichage d'un message flash d'erreur si l'e-mail est introuvable.
- Redirection vers la page d'accueil en cas d'échec de connexion.

### Tests réalisés

#### Intégration

- Connexion avec e-mail valide : affichage du tableau de bord
- Connexion avec e-mail invalide : affichage d'un message d'erreur et redirection

#### Fonctionnels

- Vérification de la redirection et du message d'erreur en cas d'e-mail inconnu
- Vérification de l'affichage correct des compétitions pour un utilisateur connecté

### Etat actuel

- Tous les tests passent
- Comportement sécurisé en cas d'entrée incorrecte
- Code prêt pour intégration continue

---

## FIX 2 : Book past competition

**Branche** : `fix/book-route-robustness`

**Objectif** :
Rendre la route de réservation plus robuste en gérant proprement les cas de club ou compétition inexistants ainsi que les compétitions déjà passées.

**Modifications** :

- Isolation de la logique métier dans des fonctions unitaires (`find_club_by_name`, `find_competition_by_name`, `is_competition_in_past`).
- Gestion explicite des erreurs de données inexistantes.
- Blocage de l'accès à la réservation pour les compétitions passées, avec affichage d'un message flash.
- Sécurisation de l'accès aux données pour éviter les erreurs d'indexation.

### Tests réalisés

#### Unitaires

- Recherche de club par nom
- Recherche de compétition par nom
- Vérification des compétitions passées

#### Intégration

- Accès à la route `/book/<competition>/<club>` avec :
  - club et compétition valides (accès autorisé)
  - club ou compétition inexistants (message d'erreur)
  - compétition passée (blocage avec message d'erreur)

#### Fonctionnels

- Parcours utilisateur complet sur la réservation :
  - Connexion
  - Accès aux compétitions valides
  - Blocage sur les compétitions passées
  - Blocage sur les réservations invalides via URL modifiée

### Etat actuel

- Tous les tests passent
- Logique de réservation entièrement sécurisée
- Code prêt pour intégration continue

---

## FIX 3 : Validation des entrées utilisateurs sur le nombre de places réservées

**Branche** : `fix/purchase-entry-validation`

**Objectif** :
Empêcher les réservations avec des entrées invalides pour le nombre de places (vides, négatives, non numériques, zéro, etc.).

**Modifications** :

- Ajout de la fonction centralisée `purchase_places_entry_validator()`.
- Rejet explicite des entrées vides, négatives, nulles ou non convertibles en entier.
- Affichage d'un message d'erreur en cas d'entrée invalide.
- Amélioration de la robustesse globale de la route `/purchasePlaces`.

### Tests réalisés

#### Intégration

- Simulation de réservations avec :
  - valeur négative
  - chaîne non numérique
  - valeur vide

- Vérification du blocage et de l'affichage des messages d'erreur

#### Fonctionnels

- Parcours complet de réservation incluant la gestion des entrées i
