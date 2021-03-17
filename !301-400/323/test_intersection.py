import pytest

from intersection import intersection


@pytest.mark.parametrize(
    "inputs,expected",
    [
        [({1, 2, 3}, {2, 3, 4}, {3, 4}), {3}],
        [([1, 2, 3, 1], {1, -1}, {}), {1}],
        [({1, "2", "3"}, {1, "3"}), {1, "3"}],
        [
            # mixing lists/sets/tuples
            ([1, 2, 3, 4, 5, 1, 2, 3, 2, 3], {0, 10, 5}, ("a", 5)),
            {
                5,
            },
        ],
        [("do you like this bite?", "i hope so"), {"o", "i", "h", "e", "s", " "}],
    ],
)
def test_basic(inputs, expected):
    results = intersection(*inputs)
    assert results == expected


@pytest.mark.parametrize(
    "inputs,expected",
    [
        [((None, "this is a string")), {" ", "a", "g", "h", "i", "n", "r", "s", "t"}],
        [
            # no input
            (None,),
            set(),
        ],
        [
            # multiple None inputs
            (None, {1, 2, 3}, None, list(range(10)), None),
            {1, 2, 3},
        ],
        [([1, 2, 3, 3, 2, 1],), {1, 2, 3}],  # single input
    ],
)
def test_edgecases(inputs, expected):
    results = intersection(*inputs)
    assert results == expected
