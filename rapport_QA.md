### Issue 1 – Sur-réservation possible

**Description**  
Empêcher un club de réserver plus de places que disponibles.

**Correction**  
Dans `/purchasePlaces`, ajout d’une condition `if placesRequired > available`  
=> `flash("You cannot book more than {available} places for this competition.")`.

**Test QA**  
`test_cannot_book_more_than_available` dans `tests/test_reservations.py`

**Vérification manuelle**  
Tentative de réservation de 9 places pour 5 disponibles → message d’erreur affiché et nombre inchangé.


### Issue 4 – Réservation pour une compétition passée

**Description** :  
Il était possible de réserver une place pour une compétition déjà terminée. Aucun blocage côté serveur n'était présent.

**Correction apportée** :  
Ajout d’une vérification dans la route `/book/<competition>/<club>` comparant la date actuelle à la date de la compétition. Si la date est passée, un message flash est affiché et la réservation est bloquée.

**Test QA automatisé** :  
`test_booking_past_competition` dans `tests/test_reservations.py`

**Vérification manuelle** :  
OK – Message d'erreur visible dans l'interface, réservation