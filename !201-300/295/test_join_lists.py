import pytest

from join_lists import join_lists


@pytest.mark.parametrize('input_list, sep, expected', [
    ([], '&', None),
    ([['a']], '|', ['a']),
    ([['a', 'b']], '&', ['a', 'b']),
    ([['a', 'b'], ['c']], '&', ['a', 'b', '&', 'c']),
    ([['a', 'b'], ['c'], ['d', 'e']], '+',
     ['a', 'b', '+', 'c', '+', 'd', 'e']),
])
def test_join_lists(input_list, sep, expected):
    assert join_lists(input_list, sep) == expected
