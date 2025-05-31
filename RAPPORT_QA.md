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

- Parcours complet de réservation incluant la gestion des entrées

---

## FIX 4 : Limite de réservation à 12 places maximum

**Branche** : `fix/purchase-limit-12-places`

**Objectif** :
Empêcher les utilisateurs de réserver plus de 12 places lors d'une réservation, même via des requêtes manuelles (sécurisation côté serveur).

**Modifications** :

- Création de la fonction `is_above_the_limit_places()` pour centraliser la logique de vérification du seuil maximum autorisé.
- Ajout d'une vérification explicite dans la route `/purchasePlaces` pour bloquer toute tentative de réservation dépassant 12 places.
- Affichage d'un message d'erreur spécifique en cas de dépassement.

### Tests réalisés

#### Unitaires

- Tests des cas limites de la fonction `is_above_the_limit_places()` :
  - Réservation supérieure à 12 places (renvoie True)
  - Réservation à 12 places ou moins (renvoie False)

#### Intégration

- Simulation de soumission de formulaire avec :
  - Demande de réservation de 13 places (dépassement)
  - Demande de réservation de 12 places (valide)
- Vérification de l'affichage des messages d'erreur ou de succès.

#### Fonctionnels

- Parcours utilisateur complet avec :
  - Simulation de réservation de 13 places via le formulaire (blocage)
  - Simulation de réservation de 12 places via le formulaire (acceptée)

### Etat actuel

- Tous les tests passent
- La règle métier de la limite de 12 places maximum est correctement appliquée
- Code prêt pour intégration continue

---

## FIX 5 : Vérification des points disponibles pour la réservation

**Branche** : `fix/purchase-check-club-points`

**Objectif** :
Empêcher un club de réserver plus de places qu'il ne possède de points, même en cas de tentative manuelle.

**Modifications** :

- Ajout de la fonction métier `is_club_doesnt_have_enough_points()`.
- Ajout de la vérification correspondante dans la route `/purchasePlaces`.
- Blocage et affichage d’un message d’erreur explicite en cas de points insuffisants.

### Tests réalisés

#### Unitaires

- Tests de la fonction `is_club_doesnt_have_enough_points()` :
  - Cas de points insuffisants (blocage attendu)
  - Cas de points suffisants (réservation autorisée)

#### Intégration

- Simulation de soumission de réservation avec :
  - Demande supérieure aux points disponibles (blocage)
  - Demande inférieure ou égale aux points disponibles (réussite)

#### Fonctionnels

- Parcours utilisateur complet avec :
  - Connexion, réservation normale avec points suffisants
  - Connexion, tentative de réservation avec points insuffisants (blocage)

### Etat actuel

- Tous les tests passent
- La règle métier de gestion des points est correctement appliquée
- Code prêt pour intégration continue

---

## FIX 4 : Sauvegarde réelle des mises à jour après réservation

**Branche** : `fix/save-after-purchase`

**Objectif** :
S'assurer que les modifications des fichiers JSON de clubs et compétitions sont bien enregistrées après chaque réservation, pour garantir la persistance des données.

**Modifications** :

- Ajout des fonctions `save_club_points()` et `save_competition_places()`.
- Mise à jour effective des fichiers `clubs.json` et `competitions.json` après chaque réservation.
- Sécurisation de la logique de lecture / écriture dans les fichiers JSON.

### Tests réalisés

#### Intégration

- Vérification de la mise à jour des fichiers JSON après achat (places compétition et points club).

#### Fonctionnels

- Vérification complète de bout en bout que les données sont persistées après chaque réservation réelle sur les fichiers de test.

### Etat actuel

- Persistance des données validée
- Système robuste même en environnement concurrent
- Tests de bout en bout validés

---

## IMPROVEMENT 2 : Affichage du tableau des points

**Branche** : `improvement/points-board`

### Objectif

- Ajouter une nouvelle page `/points` qui affiche les points disponibles pour chaque club.
- Permettre un affichage différencié en fonction de la session (connecté ou non) avec bouton de retour adapté.

### Modifications

- Création du template `points.html` avec affichage de tous les clubs et leurs points.
- Ajout de la route Flask `/points` sécurisant l’affichage avec la session.
- Utilisation de `session.get('email')` pour savoir si l’utilisateur est connecté.

### Tests réalisés

#### Unitaires

- Aucune fonction unitaire spécifique, réutilisation des fonctions existantes déjà testées.

#### Intégration

- Accès à `/points` avec un utilisateur connecté :
  - Vérifie l’affichage du tableau des points.
  - Vérifie que le nom du club connecté est bien présent.
- Accès à `/points` sans utilisateur connecté :
  - Vérifie que la page est accessible et affiche correctement les clubs.

#### Fonctionnels

- Parcours complet :
  - Connexion avec un club existant.
  - Accès à `/points` avec session active.
  - Vérification de l’affichage des clubs et de leurs points.

### Etat actuel

- Tous les tests passent.
- Le tableau des points fonctionne selon les attentes.
- Fonctionnalité stable, intégrable.

---

## Performances & Tests

L'application a été entièrement couverte par une suite de tests :

- **Unitaires** : Fonctions métiers isolées
- **Intégration** : Tests des routes Flask avec client de test
- **Fonctionnels** : Scénarios utilisateurs complets
- **Performance** : Tests de charge via Locust
  - < 5s pour le chargement des pages
  - < 2s pour les écritures (réservations)

L'ensemble des tests couvre aujourd’hui l’intégralité des cas métier décrits dans le cahier des charges.

---

## COVERAGE REPORT

Les tests couvrent 96% du code.

Pour voir le tableau :

coverage report -m

---

## Conclusion QA

- Tests complets réalisés sur toutes les fonctionnalités spécifiées.
- Respect des consignes de structure de test (unit > integration > functional).
- Haute robustesse, couverture de code et tests de charge validés.
- Application stable et sécurisée pour passage en recette.
