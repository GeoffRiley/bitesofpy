from random import sample

import pytest
from minimum_number import minimum_number


@pytest.mark.parametrize('test_input, expected', [
    ([], 0),
    ([0], 0),
    ([1], 1),
    ([5], 5),
    ([1, 1], 1),
    ([7, 1], 17),
    ([1, 7], 17),
    ([3, 2, 1], 123),
    ([1, 9, 5, 9, 1], 159),
    ([0, 9, 5, 9], 59),
    ([9, 3, 1, 2, 7, 9, 4, 5, 7, 9, 8, 6, 1], 123456789),
    ([4, 2], 24),
    ([1, 5, 2, 3, 4, 1, 4, 2, 3], 12345),
    (sample(range(1, 6), 5), 12345),
    (sample(range(0, 6), 6), 12345),
])
def test_minimum_number(test_input, expected):
    assert minimum_number(test_input) == expected
