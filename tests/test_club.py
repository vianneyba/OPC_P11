import pytest
from app.club import Club


def test_purchase_place():
    club_one = Club('Vianney Bailleux', 'vianney@free.fr', 14)
    club_two = Club('Vianney Bailleux', 'vianney@free.fr', 14)
    club_one.purchase_place(10)
    assert club_one.points == 4
    assert club_one.points != 14
    with pytest.raises(ValueError):
        club_two.purchase_place(15)
