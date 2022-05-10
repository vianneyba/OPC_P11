import json
from flask import Flask, render_template, request, redirect, flash, url_for
from app.club import Club
from app.competition import Competition
from app.load_json import loadClubs, loadCompetitions
from app.booking import Booking
from datetime import datetime, date

MAX_PLACES = 12
ERROR = {
    'COMPETITION_NOT_EXIST': 'competition does not exist',
    'CLUB_NOT_EXIST': 'club does not exist',
    'EMAIL_NOT_EXIST': 'Sorry, that email wasn\'t found.',
    'TRY_AGAIN': 'Something went wrong-please try again',
    'BOOK_IN_PAST_COMPETITION': 'you cannot book a place in a past competition!',
    'ENOUGH_PLACE_COMPETITION': 'There is not enough place on this competition',
    'ENOUGH_PLACE_CLUB': 'there is not enough place for this club',
    'RESERVED_MORE_MAX_PLACES': f'you have reserved more than {MAX_PLACES} places',
    'BOOKING_OK': 'Great-booking complete!'}

def searchClub(listClubs, clubName):
    for club in listClubs:
        if club.name == clubName:
            return club

    raise ValueError(ERROR['CLUB_NOT_EXIST'])


def searchCompetition(listCompetition, competitionName):
    for competition in listCompetition:
        if competition.name == competitionName:
            return competition

    raise ValueError(ERROR['COMPETITION_NOT_EXIST'])


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions('competitions.json')
clubs = loadClubs('clubs.json')

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
        "index.html", error=ERROR['EMAIL_NOT_EXIST']), 404


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = None
    try:
        foundClub = searchClub(clubs, club)
        foundCompetition = searchCompetition(competitions, competition)
        if datetime.now() <= foundCompetition.get_date():
            return render_template(
                'booking.html', club=foundClub, competition=foundCompetition)
        else:
            return render_template(
                'welcome.html', club=foundClub, competitions=competitions)
    except ValueError:
        flash(ERROR['TRY_AGAIN'])
        return render_template(
            'welcome.html', club=foundClub, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():

    placesRequired = int(request.form['places'])
    competition = searchCompetition(competitions, request.form['competition'])
    club = searchClub(clubs, request.form['club'])

    code = 200
    have_place = competition.enough_place(placesRequired)
    have_point = club.enough_point(placesRequired)
    have_booked = Booking.already_booked(club.name, competition.name)


    if competition.get_date() <= datetime.now():
        code = 403
        flash(ERROR ['BOOK_IN_PAST_COMPETITION'])
    elif have_place is False:
        code = 403
        flash(ERROR ['ENOUGH_PLACE_COMPETITION'])
    elif have_point is False:
        code = 403
        flash(ERROR ['ENOUGH_PLACE_CLUB'])
    elif placesRequired > MAX_PLACES or (have_booked is not None and have_booked.nb_places + placesRequired > MAX_PLACES):
        code = 403
        flash(ERROR ['RESERVED_MORE_MAX_PLACES'])
    else:
        if have_booked is None:
            Booking(club.name, competition.name, placesRequired)
        else:
            have_booked.add_places(placesRequired)

        competition.set_number_of_places(placesRequired)
        club.purchase_place(placesRequired)
        flash(ERROR ['BOOKING_OK'])

    return render_template(
        'welcome.html', club=club, competitions=competitions), code


@app.route('/displayBoard')
def displayBoard():
    return render_template('list_clubs.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
