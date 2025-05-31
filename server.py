import json, os, shutil, click

from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

# DB PATHS FOR SEED AND DB FILES
DATA_DIR = ""

CLUBS_SEED_FILE = os.path.join(DATA_DIR, "seed_clubs.json")
CLUBS_DB_FILE = os.path.join(DATA_DIR, "clubs.json")

COMPET_SEED_FILE = os.path.join(DATA_DIR, "seed_competitions.json")
COMPET_DB_FILE = os.path.join(DATA_DIR, "competitions.json")


def reset_db_from_seed():
    shutil.copyfile(CLUBS_SEED_FILE, CLUBS_DB_FILE)
    shutil.copyfile(COMPET_SEED_FILE, COMPET_DB_FILE)
    print("DB reinitialized from seed data.")


# ----- UTILS ------ #
def loadClubs(filename="clubs.json"):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("clubs", [])


def loadCompetitions(filename="competitions.json"):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("competitions", [])


def find_club_by_email(email, clubs_list):
    return next((club for club in clubs_list if club["email"] == email), None)


def find_club_by_name(name, clubs_list):
    return next((club for club in clubs_list if club["name"] == name), None)


def find_competition_by_name(name, competitions_list):
    return next(
        (compet for compet in competitions_list if compet["name"] == name),
        None,
    )


def is_competition_in_past(competition):
    try:
        competition_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
        return competition_date < datetime.now()
    except (KeyError, ValueError):
        return True  # On considère une date invalide comme passée pour la sécurité


def is_not_enough_places_available(competition, places_required):
    return int(competition["numberOfPlaces"]) < places_required


# Cette fonction fait deux choses :
# 1. Convertit la valeur en entier si c'est une chaîne de caractères
# 2. Vérifie la validité de l'entrée, nombre positif et non vide
def purchase_places_entry_validator(places_required):
    try:
        if not places_required:
            return None

        places_required = int(str(places_required).strip())

        if places_required <= 0:
            return None

        return places_required
    except (ValueError, TypeError):
        return None


# Pas besoin d'une logique de validation, purchase_places_entry_validator s'en charge
def is_above_the_limit_places(places_required, limit=12):
    return places_required > limit


def is_club_doesnt_have_enough_points(club_points, places_required):
    return int(club_points) < places_required


# ----- Flask App Setup ----- #
app = Flask(__name__)


# Reset DB with flask reset-db
@app.cli.command("reset-db")
def reset_db_cmd():
    reset_db_from_seed()
    click.echo("DB reinitialized from seed data.")


# Reset DB if in development mode
flask_env = os.getenv("FLASK_ENV", "").lower()
if flask_env == "development" and os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    reset_db_from_seed()

app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


# ----- Flask Routes ----- #
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    email = request.form.get("email")
    club = find_club_by_email(email, clubs)

    if not club:
        flash("Sorry, we could not find your email address.")
        return redirect(url_for("index"))

    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = find_club_by_name(club, clubs)
    foundCompetition = find_competition_by_name(competition, competitions)

    if not foundClub or not foundCompetition:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)

    if is_competition_in_past(foundCompetition):
        flash("You cannot book places for a past competition.")
        return render_template(
            "welcome.html", club=foundClub, competitions=competitions
        )

    return render_template("booking.html", club=foundClub, competition=foundCompetition)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    # Cette forme permet d'ajouter une robustesse en cas de non reception du champ
    placesRequired = request.form.get("places", "").strip()
    available = int(competition["numberOfPlaces"])

    places_required_int = purchase_places_entry_validator(placesRequired)

    # Même si c'est bloqué par le client, on peut passer par postman, empêche cela définitivement
    if is_competition_in_past(competition):
        flash("You cannot book places for a past competition.")
        return render_template("welcome.html", club=club, competitions=competitions)

    if places_required_int is None:
        flash("Invalid number of places entered.")
        return render_template("welcome.html", club=club, competitions=competitions)

    # La limite peut être redéfinie en 2eme paramètre, limit=12 étant la valeur par défaut
    if is_above_the_limit_places(places_required_int):
        flash("You cannot book more than 12 places at once.")
        return render_template("welcome.html", club=club, competitions=competitions)

    if is_club_doesnt_have_enough_points(club["points"], places_required_int):
        flash("You do not have enough points to book this number of places.")
        return render_template("welcome.html", club=club, competitions=competitions)

    if is_not_enough_places_available(competition, places_required_int):
        flash(f"You cannot book more than {available} places for this competition.")
        return render_template("welcome.html", club=club, competitions=competitions)

    competition["numberOfPlaces"] = available - places_required_int
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
