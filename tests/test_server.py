from app.club import Club
import server


clubs = [
    Club('virginie dupont', 'virginie@free.fr', '12'),
    Club('vianney bailleux', 'vianney@free.fr', '14')
]


def test_showSummary_email(client, mocker):
    mocker.patch.object(server, "clubs", clubs)
    response_ok = client.post(
        "/showSummary", data={"email": "vianney@free.fr"})
    response_ko = client.post(
        "/showSummary", data={"email": "aymeric@free.fr"})
    assert response_ok.status_code == 200
    assert response_ko.status_code == 404
