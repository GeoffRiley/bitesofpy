import pytest

from island import island_size

rectangle = [[0, 1, 1, 0],
             [0, 1, 1, 0],
             [0, 1, 1, 0],
             [0, 1, 1, 0]]

small = [[0, 0, 0],
         [0, 1, 0],
         [0, 0, 0]]

empty = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

whole = [[1, 1, 1],
         [1, 0, 1],
         [1, 1, 1]]


@pytest.mark.parametrize("map_, expected", [
    (rectangle, 12),
    (small, 4),
    (empty, 0),
    (whole, 16),
])
def test_island_size(map_, expected):
    assert island_size(map_) == expected
