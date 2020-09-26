import pytest

from conversion import dec_to_base


@pytest.mark.parametrize("number, base, expected", [
    (6, 2, 110), (7, 2, 111), (10, 2, 1010),
    (16, 2, 10000), (20, 2, 10100), (10, 6, 14),
    (24, 6, 40), (177, 6, 453), (256, 6, 1104),
    (1024, 6, 4424), (10, 8, 12), (24, 8, 30),
    (177, 8, 261), (256, 8, 400), (1024, 8, 2000),
    (2020, 8, 3744),
])
def test_dec_to_base(number, base, expected):
    assert dec_to_base(number, base) == expected
