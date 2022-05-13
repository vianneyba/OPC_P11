from app.club import Club
from app.competition import Competition
import server
from datetime import datetime, timedelta

clubs = [
    Club('virginie dupont', 'virginie@free.fr', '8'),
    Club('vianney bailleux', 'vianney@free.fr', '14'),
    Club('raymond bailleux', 'raymond@free.fr', '14')
]

time_test_one = datetime.now() - timedelta(minutes=50)
time_test_two = datetime.now() + timedelta(minutes=50)
competitions = [
    Competition('test_one', time_test_one.strftime("%Y-%m-%d %H:%M:%S"), '7'),
    Competition('test_two', time_test_two.strftime("%Y-%m-%d %H:%M:%S"), '20'),
    Competition('test_three', time_test_two.strftime("%Y-%m-%d %H:%M:%S"), '7'),
]


def func_test_in_response(client, data, error_message, status_code):
    response = client.post(
        "/purchasePlaces",
        data=data)
    data = response.data.decode()
    expected_data = error_message
    assert response.status_code == status_code
    assert expected_data in data


def test_showSummary_email_valid(client, mocker):
    mocker.patch.object(server, "clubs", clubs)
    response = client.post(
        "/showSummary", data={"email": "vianney@free.fr"})
    assert response.status_code == 200


def test_showSummary_email_invalid(client, mocker):
    mocker.patch.object(server, "clubs", clubs)
    response = client.post(
        "/showSummary", data={"email": "aymeric@free.fr"})
    assert response.status_code == 404


def test_purchasePlaces_enough_place_competition(client, mocker):
    mocker.patch.object(server, "clubs", clubs)
    mocker.patch.object(server, "competitions", competitions)

    data = {
        "competition": "test_three",
        "club": "vianney bailleux",
        "places": "8"}
    func_test_in_response(
        client, data, server.ERROR['ENOUGH_PLACE_COMPETITION'], 403)


def test_purchasePlaces_enough_points_club(client, mocker):
    mocker.patch.object(server, "clubs", clubs)
    mocker.patch.object(server, "competitions", competitions)

    data = {
        "competition": "test_two",
        "club": "virginie dupont",
        "places": "9"}
    func_test_in_response(client, data, server.ERROR['ENOUGH_PLACE_CLUB'], 403)


def test_purchasePlaces_reserved_max_place(client, mocker):
    mocker.patch.object(server, "clubs", clubs)
    mocker.patch.object(server, "competitions", competitions)

    data = {
        "competition": "test_two",
        "club": "vianney bailleux",
        "places": "14"}
    func_test_in_response(
        client, data, server.ERROR['RESERVED_MORE_MAX_PLACES'], 403)


def test_purchasePlaces(client, mocker):
    mocker.patch.object(server, "clubs", clubs)
    mocker.patch.object(server, "competitions", competitions)

    data = {
        "competition": "test_two",
        "club": "vianney bailleux",
        "places": "3"}
    func_test_in_response(client, data, server.ERROR['BOOKING_OK'], 200)


def test_purchasePlaces_reserved_max_place_two(client, mocker):
    mocker.patch.object(server, "clubs", clubs)
    mocker.patch.object(server, "competitions", competitions)

    data = {
        "competition": "test_two",
        "club": "raymond bailleux",
        "places": "4"}
    func_test_in_response(client, data, server.ERROR['BOOKING_OK'], 200)
    data = {
        "competition": "test_two",
        "club": "raymond bailleux",
        "places": "9"}
    func_test_in_response(
        client, data, server.ERROR['RESERVED_MORE_MAX_PLACES'], 403)


def test_purchasePlaces_competition_date_in_past(client, mocker):
    mocker.patch.object(server, "clubs", clubs)
    mocker.patch.object(server, "competitions", competitions)

    data = {
        "competition": "test_one",
        "club": "vianney bailleux",
        "places": "1"}
    func_test_in_response(
        client, data, server.ERROR['BOOK_IN_PAST_COMPETITION'], 403)


def test_purchasePlaces_competition_date_in_future(client, mocker):
    mocker.patch.object(server, "clubs", clubs)
    mocker.patch.object(server, "competitions", competitions)

    data = {
        "competition": "test_two",
        "club": "vianney bailleux",
        "places": "1"}
    func_test_in_response(client, data, server.ERROR['BOOKING_OK'], 200)


def test_displayBoard(client, mocker):
    clubs = [
        Club('club 1', 'club1@free.fr', '9'),
        Club('club 2', 'club2@free.fr', '6')]

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


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_book_competition_not_exist(client, mocker):
    mocker.patch.object(server, "clubs", clubs)
    mocker.patch.object(server, "competitions", competitions)

    response = client.get("/book/club%201/virginie%20dupont")
    assert response.status_code == 404


def test_book_club_not_exist(client, mocker):
    mocker.patch.object(server, "clubs", clubs)
    mocker.patch.object(server, "competitions", competitions)

    response = client.get("/book/test_three/marie%20dupont")
    assert response.status_code == 404


def test_book_competition_date_in_past(client, mocker):
    mocker.patch.object(server, "clubs", clubs)
    mocker.patch.object(server, "competitions", competitions)

    response = client.get("/book/test_one/virginie%20dupont")
    assert response.status_code == 403


def test_book_ok(client, mocker):
    mocker.patch.object(server, "clubs", clubs)
    mocker.patch.object(server, "competitions", competitions)

    response = client.get("/book/test_three/virginie%20dupont")
    assert response.status_code == 200


def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302
