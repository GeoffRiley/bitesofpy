import pytest

from search_apartment import search_apartment


@pytest.mark.parametrize(
    "buildings, direction, expected",
    [
        ([1, 1, 1, 1, 1], "W", [0]),
        ([2, 1, 1, 1, 1], "E", [0, 4]),
        ([3, 5, 4, 3, 3, 1], "W", [0, 1]),
        ([3, 5, 4, 3, 3, 1], "E", [1, 2, 4, 5]),
        ([3, 5, 4, 4, 7, 1, 3, 2], "W", [0, 1, 4]),
        ([3, 5, 4, 4, 7, 1, 3, 2], "E", [4, 6, 7]),
        ([1, 5, 4, 4, 5, 6, 6, 1], "W", [0, 1, 5]),
        ([1, 5, 4, 4, 5, 6, 6, 1], "E", [6, 7]),
        ([7, 5, 4, 4, 5, 6, 6, 5, 8], "W", [0, 8]),
        ([7, 5, 4, 4, 5, 6, 6, 5, 8], "E", [8]),
        ([1, 2, 3, 3, 4, 4, 4, 5], "W", [0, 1, 2, 4, 7]),
        ([1, 2, 3, 3, 4, 4, 4, 5], "E", [7]),
    ],
)
def test_search_apartment(buildings, direction, expected):
    assert search_apartment(buildings, direction) == expected
