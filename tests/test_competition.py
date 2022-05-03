import pytest
from app.competition import Competition


def test_purchase_place():
    competition_one = Competition('Spring Festival', '2020-03-27 10:00:00', 25)
    competition_one.set_number_of_places(10)
    assert competition_one.numberOfPlaces == 15
    with pytest.raises(ValueError):
        competition_one.set_number_of_places(30)
