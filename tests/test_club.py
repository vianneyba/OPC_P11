import pytest
from app.club import Club

COEF = 2


def test_purchase_place():
    nbr_points = 14
    nbr_place = 3
    club_one = Club('Vianney Bailleux', 'vianney@free.fr', nbr_points)
    club_two = Club('Vianney Bailleux', 'vianney@free.fr', nbr_points)
    club_one.purchase_place(3, COEF)
    assert club_one.points == nbr_points - nbr_place * COEF
    assert club_one.points != 14
    with pytest.raises(ValueError):
        club_two.purchase_place(15, COEF)
