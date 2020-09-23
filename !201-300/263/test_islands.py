import pytest

from islands import count_islands

squares = [[1, 1, 0, 1],
           [1, 1, 0, 1],
           [0, 0, 1, 1],
           [1, 1, 1, 0]]

sparse = [[1, 0, 1],
          [0, 1, 0],
          [1, 0, 1]]

empty = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

bad_map = [[]]

circles = [[1, 1, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 1],
           [1, 0, 0, 0, 1, 1],
           [1, 0, 0, 0, 1, 0],
           [1, 0, 0, 1, 1, 0],
           [1, 1, 1, 1, 0, 0]]


@pytest.mark.parametrize("data, expected", [
    (squares, 2),
    (sparse, 5),
    (empty, 0),
    (bad_map, 0),
    (circles, 1),
])
def test_count_islands(data, expected):
    assert count_islands(data) == expected
