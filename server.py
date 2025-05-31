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
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("clubs", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading clubs data: {e}")
        return []


def loadCompetitions(filename="competitions.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("competitions", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading competitions data: {e}")
        return []


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


def places_json_update(competition, places_required):
    """
    Update the number of places available for a competition.
    """
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - places_required
    return competition


def save_club_points(filename="clubs.json", clubs_data=None):
    if clubs_data is None:
        clubs_data = clubs

    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"clubs": clubs_data}, f, indent=4, ensure_ascii=False)


def save_competition_places(filename="competitions.json", competitions_data=None):
    if competitions_data is None:
        competitions_data = competitions

    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"competitions": competitions_data}, f, indent=4, ensure_ascii=False)


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


# ----- Flask Routes ----- #
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    clubs = loadClubs(CLUBS_DB_FILE)
    competitions = loadCompetitions(COMPET_DB_FILE)

    email = request.form.get("email")
    club = find_club_by_email(email, clubs)

    if not club:
        flash("Sorry, we could not find your email address.")
        return redirect(url_for("index"))

    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    clubs = loadClubs(CLUBS_DB_FILE)
    competitions = loadCompetitions(COMPET_DB_FILE)

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
    clubs = loadClubs(CLUBS_DB_FILE)
    competitions = loadCompetitions(COMPET_DB_FILE)

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

    club["points"] = str(int(club["points"]) - places_required_int)
    competition["numberOfPlaces"] = str(available - places_required_int)

    save_club_points(CLUBS_DB_FILE, clubs)
    save_competition_places(COMPET_DB_FILE, competitions)

    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
