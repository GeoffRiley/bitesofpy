import pytest

from pascal import pascal


@pytest.mark.parametrize("arg, expected", [
    (0, []),
    (1, [1]),
    (2, [1, 1]),
    (5, [1, 4, 6, 4, 1]),
    (10, [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]),
    (12, [1, 11, 55, 165, 330, 462, 462, 330, 165, 55, 11, 1]),
    (6, [1, 5, 10, 10, 5, 1]),
])
def test_pascal(arg, expected):
    assert pascal(arg) == expected
