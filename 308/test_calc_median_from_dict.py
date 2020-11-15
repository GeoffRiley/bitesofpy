import pytest
from calc_median_from_dict import calc_median_from_dict


# Small Numbers
@pytest.mark.parametrize(
    "test_input,expected",
    [
        ({1: 1}, 1),
        ({1: 1, 2: 1}, 1.5),
        ({1: 2, 2: 1, 3: 2}, 2),
        ({2: 1, 1: 2, 3: 2}, 2),
        ({1.5: 2, 2.5: 2}, 2),
        ({1.75: 2, 2.25: 2}, 2),
        ({-1: 22, +4: 22}, 1.5),
    ],
)
def test_median_from_dict__valid_numbers(test_input, expected):
    assert calc_median_from_dict(test_input) == expected


# Huge numbers
@pytest.mark.parametrize(
    "test_input,expected",
    [
        ({1: 1_000_000_000_000_000, 2: 1, 3: 1_000_000_000_000_000}, 2),
        ({1: 1_000_000_000_000_000, 3: 1_000_000_000_000_000}, 2),
        (
                {
                    0: 800_000_000,
                    1: 200_000_000,
                    2: 200_000_000,
                    3: 200_000_000,
                    4: 200_000_000,
                    5: 1_000_000_000,
                    6: 20_000_000_000,
                    7: 4_000_000_000,
                    8: 8_000_000_000,
                    9: 16_000_000_000,
                },
                7,
        ),
    ],
)
def test_median_from_dict_valid_huge_numbers(test_input, expected):
    assert calc_median_from_dict(test_input) == expected


# Errors should be raised when the dict value is not a number
@pytest.mark.parametrize(
    "test_input",
    [
        ({1: "a"}),
        ({3: []}),
    ],
)
def test_median_from_dict_raises_error(test_input):
    with pytest.raises(TypeError):
        calc_median_from_dict(test_input)
