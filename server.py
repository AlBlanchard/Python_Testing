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


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    matching_clubs = [c for c in clubs if c["email"] == request.form["email"]]

    if not matching_clubs:
        flash("Sorry, we could not find your email address.")
        return redirect(url_for("index"))

    club = matching_clubs[0]
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]

    competition_date = datetime.strptime(foundCompetition["date"], "%Y-%m-%d %H:%M:%S")

    if competition_date < datetime.now():
        flash("You cannot book places for a past competition.")
        return render_template(
            "welcome.html", club=foundClub, competitions=competitions
        )

    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])
    if placesRequired > 12:
        flash("You cannot book more than 12 places at a time.")
        return render_template("welcome.html", club=club, competitions=competitions)

    available = int(competition["numberOfPlaces"])
    points_required = placesRequired * 3
    club_points = int(club["points"])

    if placesRequired > available:
        flash(f"You cannot book more than {available} places for this competition.")
        return render_template("welcome.html", club=club, competitions=competitions)

    if points_required > club_points:
        flash(f"You do not have enough points to book {placesRequired} places.")
        return render_template("welcome.html", club=club, competitions=competitions)

    competition["numberOfPlaces"] = available - placesRequired
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
