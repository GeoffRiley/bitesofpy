import pytest

from ops import num_ops


@pytest.mark.parametrize('test_input, expected', [
    (10, 6), (12, 9), (15, 17),
    (33, 18), (55, 24), (102, 25),
    (1985, 42), (2020, 24), (3012, 22)
])
def test_num_ops(test_input, expected):
    assert num_ops(test_input) == expected
