# Documentation des tests

## Structure des tests

Le dossier `tests/` est organisé selon trois niveaux de tests :

- `tests/unit/` :  
  Tests unitaires des fonctions métiers pures et isolées.

- `tests/integration/` :  
  Tests d'intégration des routes Flask, vérifiant les réponses HTTP et les comportements des vues.

- `tests/functional/` :  
  Tests fonctionnels simulant des scénarios utilisateurs complets, avec base de données JSON isolée.

- `tests/utils.py` :  
  Fonctions utilitaires de tests partagées (ex: connexion utilisateur, gestion des dates).

- `tests/conftest.py` :  
  Toutes les fixtures centralisées pour pytest.

## Gestion des fixtures

### 1. `test_data`

- Fournit les jeux de données utilisés dans tous les tests.
- Défini directement dans `conftest.py` sous forme de dictionnaires Python.

### 2. `patch_server_data`

- Utilisé dans les tests unitaires et d'intégration.
- Permet de patcher en mémoire les variables globales `clubs` et `competitions` de l'application Flask.
- A appeler explicitement dans les tests concernés.

### 3. `isolated_test_db`

- Active automatiquement pour les tests fonctionnels.
- Crée des fichiers JSON temporaires à chaque test pour simuler la base de données de l'application.
- Garantit l'isolation des tests fonctionnels et permet de tester les modifications de données.

### 4. `client`

- Fournit un client Flask de test configuré en mode `TESTING`.

## Lancement des tests

Depuis la racine du projet, exécuter simplement :

```bash
pytest
```
