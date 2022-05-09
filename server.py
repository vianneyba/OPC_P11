import json
from flask import Flask, render_template, request, redirect, flash, url_for
from app.club import Club
from app.competition import Competition


def loadClubs():
    clubs = []
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        for c in listOfClubs:
            club = Club(c['name'], c['email'], c['points'])
            clubs.append(club)
        return clubs


def loadCompetitions():
    competitions = []
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        for c in listOfCompetitions:
            competition = Competition(
                c['name'], c['date'], c['numberOfPlaces'])
            competitions.append(competition)
        return competitions


def searchClub(listClubs, clubName):
    for club in listClubs:
        if club.name == clubName:
            return club

    raise ValueError("club does not exist")


def searchCompetition(listCompetition, competitionName):
    for competition in listCompetition:
        if competition.name == competitionName:
            return competition

    raise ValueError("competition does not exist")


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    for c in clubs:
        if c.email == request.form['email']:
            club = c
            return render_template(
                'welcome.html', club=club, competitions=competitions)

    return render_template(
        "index.html", error="Sorry, that email wasn't found."), 404


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = None
    try:
        foundClub = searchClub(clubs, club)
        foundCompetition = searchCompetition(competitions, competition)
        return render_template(
            'booking.html', club=foundClub, competition=foundCompetition)
    except ValueError:
        flash("Something went wrong-please try again")
        return render_template(
            'welcome.html', club=foundClub, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():

    placesRequired = int(request.form['places'])
    competition = searchCompetition(competitions, request.form['competition'])
    club = searchClub(clubs, request.form['club'])

    have_place = competition.enough_place(placesRequired)
    have_point = club.enough_point(placesRequired)

    if have_place and have_point:
        competition.set_number_of_places(placesRequired)
        club.purchase_place(placesRequired)
    else:
        flash('Great-booking complete!')

    return render_template(
        'welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
