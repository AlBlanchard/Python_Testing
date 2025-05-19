### Issue 1 – Sur-réservation possible

**Description**  
Empêcher un club de réserver plus de places que disponibles.

**Correction**  
Dans `/purchasePlaces`, ajout d'une condition `if placesRequired > available`  
=> `flash("You cannot book more than {available} places for this competition.")`.

**Test QA**  
`test_cannot_book_more_than_available` dans `tests/test_reservations.py`

**Vérification manuelle**  
Tentative de réservation de 9 places pour 5 disponibles => message d'erreur affiché et nombre inchangé.

### Issue 2 – Usage excessif de points

**Description**  
Un club pouvait dépenser plus de points que ceux dont il dispose (coût = 3 points/place).

**Correction**  
Dans `/purchasePlaces` :
- Calcul de `pointsRequired = placesRequired * 3`
- Comparaison avec `club["points"]`  
- `flash("You don't have enough points to book X places.")` si insuffisant

**Test QA**  
`test_cannot_use_more_points_than_available` dans `tests/test_reservations.py`

**Vérification manuelle**  
Tenter de réserver 2 places (6 points) avec seulement 4 points => message d'erreur et points inchangés.

### Issue 3 – Limite de 12 places par compétition

**Description**  
Un club pouvait réserver plus de 12 places, ce qui viole la règle métier.

**Correction**  
Dans `/purchasePlaces`, ajout d'une condition `if placesRequired > 12`

**Test QA**
`test_cannot_book_more_than_12_places` dans `tests/test_booking_limits.py`

**Vérification manuelle** :  
Tenter de réserver 13 places (en ayant suffisament de points) => message d'erreur

### Issue 4 – Réservation pour une compétition passée

**Description** :  
Il était possible de réserver une place pour une compétition déjà terminée. Aucun blocage côté serveur n'était présent.

**Correction apportée** :  
Ajout d'une vérification dans la route `/book/<competition>/<club>` comparant la date actuelle à la date de la compétition. Si la date est passée, un message flash est affiché et la réservation est bloquée.

**Test QA automatisé** :  
`test_booking_past_competition` dans `tests/test_reservations.py`

**Vérification manuelle** :  
OK – Message d'erreur visible dans l'interface, réservation