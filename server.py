import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


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


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


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
    placesRequired = int(request.form["places"])
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
