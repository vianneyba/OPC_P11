from selenium import webdriver
from selenium.webdriver.common.by import By
from server import COEF

url_serveur = 'http://localhost:8083'
coef_pts = 1


def init_selenium():
    binary = 'tests/geckodriver'
    driver = webdriver.Firefox(executable_path=binary)

    driver.get(url_serveur)

    return driver


def login(driver, email):
    driver.find_element(by=By.TAG_NAME, value='input').send_keys(email)
    driver.find_element(by=By.TAG_NAME, value='button').click()


def search_competition(driver, name, club):
    links = driver.find_elements(by=By.TAG_NAME, value='a')
    url = f'{url_serveur}/book/{name}/{club}'
    for link in links:
        if link.get_attribute("href").replace("%20", " ") == url:
            link.click()
            break


def book_place(driver, nbr):
    driver.find_element(by=By.NAME, value='places').send_keys(nbr)
    driver.find_elements(by=By.TAG_NAME, value='button')[0].click()


def get_pts_by_id(driver):
    return driver.find_element(by=By.ID, value='points').text


def get_pts_for_competiton(driver):
    return driver.find_elements(by=By.CLASS_NAME, value='pts_club')[2].text


def test_book_place(client, mocker):
    pts_club = 12
    pts_competiton = 15
    email_club = 'vianney@free.fr'
    name_club = 'vianney bailleux'
    competition = 'Test Competition One'
    nb_places = 2

    driver = init_selenium()

    login(driver, email_club)
    assert f'{url_serveur}/showSummary' == driver.current_url
    assert int(get_pts_by_id(driver)) == pts_club
    assert int(get_pts_for_competiton(driver)) == pts_competiton

    search_competition(driver, competition, name_club)
    assert f'{url_serveur}/book/{competition}/{name_club}' == driver.current_url.replace('%20', ' ')
    assert int(get_pts_by_id(driver)) == pts_competiton

    book_place(driver, nb_places)
    assert int(get_pts_by_id(driver)) == pts_club - nb_places * coef_pts
    assert int(get_pts_for_competiton(driver)) == pts_competiton - nb_places

    driver.close()
