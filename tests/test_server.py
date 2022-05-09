from app.club import Club
from app.competition import Competition
import server
from datetime import datetime, timedelta 

clubs = [
    Club('virginie dupont', 'virginie@free.fr', '8'),
    Club('vianney bailleux', 'vianney@free.fr', '14')
]

time_test_one = datetime.now() - timedelta(minutes=50)
time_test_two = datetime.now() + timedelta(minutes=50)
competitions = [
    Competition('test_one', time_test_one.strftime("%Y-%m-%d %H:%M:%S"), '7'),
    Competition('test_two', time_test_two.strftime("%Y-%m-%d %H:%M:%S"), '20'),
    Competition('test_three', time_test_two.strftime("%Y-%m-%d %H:%M:%S"), '7'),
]


def test_showSummary_email(client, mocker):
    mocker.patch.object(server, "clubs", clubs)
    response_ok = client.post(
        "/showSummary", data={"email": "vianney@free.fr"})
    response_ko = client.post(
        "/showSummary", data={"email": "aymeric@free.fr"})
    assert response_ok.status_code == 200
    assert response_ko.status_code == 404

def test_purchasePlaces(client, mocker):
    mocker.patch.object(server, "clubs", clubs)
    mocker.patch.object(server, "competitions", competitions)

    response = client.post(
        "/purchasePlaces",
        data={"competition": "test_three", "club": "vianney bailleux", "places": "8"})
    data = response.data.decode()
    expected_data = "There is not enough place on this competition"
    assert response.status_code == 403
    assert expected_data in data

    response = client.post(
        "/purchasePlaces",
        data={"competition": "test_two", "club": "virginie dupont", "places": "9"})

    data = response.data.decode()
    expected_data = "there is not enough place for this club"
    assert response.status_code == 403
    assert expected_data in data

    response = client.post(
        "/purchasePlaces",
        data={"competition": "test_two", "club": "vianney bailleux", "places": "14"})
    data = response.data.decode()
    expected_data = "you have reserved more than 12 places"
    assert response.status_code == 403
    assert expected_data in data

    response = client.post(
        "/purchasePlaces",
        data={"competition": "test_two", "club": "vianney bailleux", "places": "10"})
    data = response.data.decode()
    expected_data = "Great-booking complete!"
    assert response.status_code == 200
    assert expected_data in data

    response = client.post(
        "/purchasePlaces",
        data={"competition": "test_two", "club": "vianney bailleux", "places": "3"})
    data = response.data.decode()
    expected_data = "you have reserved more than 12 places"
    assert response.status_code == 403
    assert expected_data in data

def test_purchasePlaces_date(client, mocker):
    mocker.patch.object(server, "clubs", clubs)
    mocker.patch.object(server, "competitions", competitions)

    response = client.post(
        "/purchasePlaces",
        data={"competition": "test_one", "club": "vianney bailleux", "places": "1"})
    data = response.data.decode()
    expected_data = "you cannot book a place in a past competition!"
    assert response.status_code == 403
    assert expected_data in data

    response = client.post(
        "/purchasePlaces",
        data={"competition": "test_two", "club": "vianney bailleux", "places": "1"})
    data = response.data.decode()
    expected_data = "Great-booking complete!"
    assert response.status_code == 200
    assert expected_data in data

def test_displayBoard(client, mocker):
    clubs = [
        Club('club 1', 'club1@free.fr', '9'),
        Club('club 2', 'club2@free.fr', '6')
    ]
    mocker.patch.object(server, "clubs", clubs)
    response = client.get("/displayBoard")
    data = response.data.decode()

    assert response.status_code == 200

    club_1_name = "<td>club 1</td>"
    club_1_pts = "<td>9</td>"
    club_2_name = "<td>club 2</td>"
    club_2_pts = "<td>6</td>"
    assert club_1_name in data
    assert club_1_pts in data
    assert club_2_name in data
    assert club_2_pts in data

