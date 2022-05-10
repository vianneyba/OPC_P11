import json
from app.club import Club
from app.competition import Competition

def loadClubs(clubsJson):
    clubs = []
    with open(clubsJson) as c:
        listOfClubs = json.load(c)['clubs']
        for c in listOfClubs:
            club = Club(c['name'], c['email'], c['points'])
            clubs.append(club)
        return clubs


def loadCompetitions(competitionsJson):
    competitions = []
    with open(competitionsJson) as comps:
        listOfCompetitions = json.load(comps)['competitions']
        for c in listOfCompetitions:
            competition = Competition(
                c['name'], c['date'], c['numberOfPlaces'])
            competitions.append(competition)
        return competitions