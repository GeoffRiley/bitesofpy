import pytest

from citation_indexes import i10_index, h_index, TYPE_ERROR_MSG, VALUE_ERROR_MSG

TYPE_ERRORS = [
    0,
    "0,1,2",
    "xyz",
]

VALUE_ERRORS = [
    [],
    (),
    None,
    list("abc"),
    (-1, 2, 3),
]


@pytest.mark.parametrize(
    "citations,expected",
    [
        ([0, 0, 1, 1, 10, 5, 11, 13], 3),
        ([0, 0, 1, 1, 10, 5, 1, 3], 1),
        (list(range(0, 10)), 0),
        ((0, 0, 1, 1), 0),
        ((1000, 10, 9, 1, 10, 5, 1, 3), 3),
        ([0] * 5, 0),
    ],
)
def test_i10_index(citations, expected):
    assert i10_index(citations) == expected


@pytest.mark.parametrize("citations", TYPE_ERRORS)
def test_i10_index_type_errors(citations):
    with pytest.raises(TypeError) as exc_info:
        i10_index(citations)
    assert str(exc_info.value) == TYPE_ERROR_MSG


@pytest.mark.parametrize("citations", VALUE_ERRORS)
def test_i10_index_value_errors(citations):
    with pytest.raises(ValueError) as exc_info:
        i10_index(citations)
    assert str(exc_info.value) == VALUE_ERROR_MSG


@pytest.mark.parametrize(
    "citations,expected",
    [
        ([0, 0, 1, 1, 10, 5, 11, 13], 4),
        ([0, 0, 1, 1, 10, 5, 1, 3], 3),
        (list(range(0, 10)), 5),
        ((0, 0, 1, 1), 1),
        ((1000, 10, 9, 1, 10, 5, 1, 3), 5),
        ([0] * 5, 0),
    ],
)
def test_h_index(citations, expected):
    assert h_index(citations) == expected


@pytest.mark.parametrize("citations", TYPE_ERRORS)
def test_h_index_type_errors(citations):
    with pytest.raises(TypeError) as exc_info:
        h_index(citations)
    assert str(exc_info.value) == TYPE_ERROR_MSG


@pytest.mark.parametrize("citations", VALUE_ERRORS)
def test_h_index_value_errors(citations):
    with pytest.raises(ValueError) as exc_info:
        h_index(citations)
    assert str(exc_info.value) == VALUE_ERROR_MSG
