import pytest

from two_dice_advantage import new_expected_value, original_expected_value


@pytest.mark.parametrize(
    "n, expected",
    [
        (6, 3.5),
        (10, 5.5),
        (20, 10.5),
    ],
)
def test_original_expected_value(n, expected) -> None:
    actual = original_expected_value(n)
    assert actual == expected


@pytest.mark.parametrize(
    "n, expected",
    [
        (6, 4.472),
        (10, 7.150),
        (20, 13.825),
    ],
)
def test_new_expected_value(n, expected) -> None:
    actual = new_expected_value(n)
    assert actual == expected
