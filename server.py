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
                ['name'], c['date'], c['numberOfPlaces'])
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
        "index.html", error="unknown email"), 404


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
    for c in competitions:
        if c['name'] == request.form['competition']:
            competition = c

    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(
        competition['numberOfPlaces'])-placesRequired

    for c in clubs:
        if c['name'] == request.form['club']:
            club = c

    flash('Great-booking complete!')
    return render_template(
        'welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
