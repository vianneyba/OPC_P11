from app.club import Club
from app.competition import Competition
import server
from datetime import datetime, timedelta


def test_login_logout(client, mocker):
    clubs = [Club('vianney bailleux', 'vianney@free.fr', '10')]
    mocker.patch.object(server, "clubs", clubs)
    res_login_page = client.get("/")
    res_login = client.post(
        "/showSummary", data={"email": "vianney@free.fr"})
    res_logout = client.get('/logout')

    assert res_login_page.status_code == 200
    assert res_login.status_code == 200
    assert res_logout.status_code == 302


def test_login_purchase(client, mocker):
    nbr_places = 1
    club_pts = 10
    clubs = [Club('vianney bailleux', 'vianney@free.fr', club_pts)]
    time = datetime.now() + timedelta(minutes=50)
    competitions = [
        Competition('summer', time.strftime("%Y-%m-%d %H:%M:%S"), '7')
    ]

    mocker.patch.object(server, "clubs", clubs)
    mocker.patch.object(server, "competitions", competitions)

    res_login_page = client.get("/")
    res_login = client.post(
        "/showSummary", data={"email": "vianney@free.fr"})
    response = client.post(
        "/purchasePlaces",
        data={'places': nbr_places, 'club': 'vianney bailleux', 'competition': 'summer'}
        )

    assert res_login_page.status_code == 200
    assert res_login.status_code == 200
    assert response.status_code == 200
    assert server.clubs[0].points == club_pts - nbr_places * server.COEF
    assert server.competitions[0].numberOfPlaces == 6
