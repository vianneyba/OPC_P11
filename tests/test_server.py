from app.club import Club
from app.competition import Competition
import server


clubs = [
    Club('virginie dupont', 'virginie@free.fr', '8'),
    Club('vianney bailleux', 'vianney@free.fr', '14')
]

competitions = [
    Competition('test_one', '2020-10-22 13:30:00', '7'),
    Competition('test_two', '2020-10-22 13:30:00', '20')
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
        data={"competition": "test_one", "club": "vianney bailleux", "places": "8"})
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
