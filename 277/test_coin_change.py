import pytest

from coin_change import make_changes

british = [1, 2, 5, 10, 20, 50]
usa = [1, 5, 10, 25, 50]


@pytest.mark.parametrize("change, country, expected", [
    (3, british, 2), (5, british, 4),
    (11, british, 12), (15, british, 22),
    (20, british, 41), (36, british, 175),
    (52, british, 508), (57, british, 670),
    (77, british, 1802), (3, usa, 1),  # usa 1
    (5, usa, 2), (12, usa, 4),
    (15, usa, 6), (20, usa, 9),
    (36, usa, 24), (57, usa, 62),
    (77, usa, 134), (100, usa, 292),
    (107, usa, 335),
])
def test_coin(change, country, expected):
    assert make_changes(change, country) == expected
