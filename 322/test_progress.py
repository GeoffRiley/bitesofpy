import pytest
from freezegun import freeze_time

from progress import ontrack_reading


@pytest.mark.parametrize("args, expected", [
    ((60, 2, 3), True),
    ((60, 0, 3), False),
    ((60, 0.5, 3), True),
    ((30, 16, 180), True),
    ((30, 8, 180), False),
    ((40, 1, 40), False),
    ((40, 10, 40), True),
    ((10, 10, 300), True),
    ((10, 8, 300), False),
    ((10, 8.2, 300), False),
    ((10, 8.22, 300), True),
    ((10, 10, 365), True),
])
def test_ontrack_reading(args, expected):
    assert ontrack_reading(*args) == expected


@freeze_time('2021-07-09')
def test_without_days_arg_current_date_july():
    assert ontrack_reading(60, 31) is False
    assert ontrack_reading(60, 34) is True


@freeze_time('2021-12-09')
def test_without_days_arg_current_date_december():
    assert ontrack_reading(30, 28) is False
    assert ontrack_reading(30, 29) is True
