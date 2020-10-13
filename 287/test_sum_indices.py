import pytest

from sum_indices import sum_indices


@pytest.mark.parametrize('test_input, expected', [
    ([], 0),
    (['a'], 0),
    (['a', 'b', 'c'], 3),
    (['a', 'b', 'b', 'c'], 7),
    (['a', 'b', 'b', 'c', 'a', 'b', 'a'], 29),
    (['a', 'b', 'c', 'd', 'e', 'a', 'f', 'a', 'g', 'd', 'a'], 75),
    (['a', 'b', 'z', 'c', 'd', 'x', 'b', 'x', 'e'], 42), ])
def test_sum_indices(test_input, expected):
    assert sum_indices(test_input) == expected
