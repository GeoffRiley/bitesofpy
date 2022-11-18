from datetime import datetime

import pytest

from crontab import CrontabScheduler


@pytest.fixture
def first_of_june():
    return datetime(2022, 6, 1, 12, 12)


@pytest.fixture
def day_in_june():
    return datetime(2022, 6, 28, 19, 49)


@pytest.mark.parametrize(
    "cron_expr, expected",
    [
        pytest.param("* * * *", datetime(2022, 6, 1, 12, 13), id="every minute"),
        pytest.param("1 * * *", datetime(2022, 6, 1, 13, 1), id="every first minute"),
        pytest.param(
            "10 * * *", datetime(2022, 6, 1, 13, 10), id="10th minute every hour"
        ),
        pytest.param("* 1 * *", datetime(2022, 6, 2, 1, 0), id="every first hour"),
        pytest.param("* 5 * *", datetime(2022, 6, 2, 5, 0), id="every fifth hour"),
        pytest.param("* * 1 *", datetime(2022, 6, 1, 12, 13), id="every first day"),
        pytest.param("* * 21 *", datetime(2022, 6, 21, 0, 0), id="every 21th day"),
        pytest.param("* * * 1", datetime(2023, 1, 1, 0, 0), id="every first month"),
        pytest.param("* * * 12", datetime(2022, 12, 1, 0, 0), id="every 12th month"),
    ],
)
def test_next_datetime_with_single_value(cron_expr, first_of_june, expected):
    it = CrontabScheduler(cron_expr, first_of_june)
    assert next(it) == expected


@pytest.mark.parametrize(
    "cron_expr, expected",
    [
        pytest.param("5 0 * 8", datetime(2022, 8, 1, 0, 5), id="At 00:05 in August."),
        pytest.param(
            "15 14 1 *", datetime(2022, 7, 1, 14, 15), id="At 14:15 on day-of-month 1."
        ),
        pytest.param(
            "1 1 1 1",
            datetime(2023, 1, 1, 1, 1),
            id="At 01:01 on day-of-month 1 in January.",
        ),
        pytest.param(
            "59 23 31 7",
            datetime(2022, 7, 31, 23, 59),
            id="At 23:59 on day-of-month 31 in July.",
        ),
    ],
)
def test_next_datetime_with_multiple_single_values(cron_expr, day_in_june, expected):
    it = CrontabScheduler(cron_expr, day_in_june)
    assert next(it) == expected


@pytest.mark.parametrize(
    "cron_expr, expected",
    [
        pytest.param(
            "* 1-5 * *",
            datetime(2022, 6, 2, 1, 0),
            id="At every minute past every hour from 1 through 5.",
        ),
        pytest.param(
            "0 10-20 * *",
            datetime(2022, 6, 1, 13, 0),
            id="At minute 0 past every hour from 10 through 20.",
        ),
        pytest.param(
            "0 4 8-14 *",
            datetime(2022, 6, 8, 4, 0),
            id="At 04:00 on every day-of-month from 8 through 14.",
        ),
        pytest.param(
            "0 22 * 1-5",
            datetime(2023, 1, 1, 22, 0),
            id="At 22:00 in every month from January through May.",
        ),
    ],
)
def test_next_datetime_with_range_values(cron_expr, first_of_june, expected):
    it = CrontabScheduler(cron_expr, first_of_june)
    assert next(it) == expected


@pytest.mark.parametrize(
    "cron_expr, expected",
    [
        pytest.param(
            "0 0,12 1 *",
            datetime(2022, 7, 1, 0, 0),
            id="At minute 0 past hour 0 and 12 on day-of-month 1.",
        ),
        pytest.param(
            "0 0 1,15 *",
            datetime(2022, 7, 1, 0, 0),
            id="At 00:00 on day-of-month 1 and 15.",
        ),
        pytest.param(
            "10,20,30,40,50 20,21,22,23 5,6,7 1,2,3",
            datetime(2023, 1, 5, 20, 10),
            id="At minute 10, 20, 30, 40, and 50 past hour 20, 21, 22, and 23 on day-of-month 5, 6, and 7 in January, February, and March.",
        ),
        pytest.param(
            "40,50 18,19,20 * *",
            datetime(2022, 6, 28, 19, 50),
            id="At minute 40 and 50 past hour 18, 19, and 20.",
        ),
    ],
)
def test_next_datetime_with_list_values(cron_expr, day_in_june, expected):
    it = CrontabScheduler(cron_expr, day_in_june)
    assert next(it) == expected


@pytest.mark.parametrize(
    "cron_expr, expected",
    [
        pytest.param(
            "0 0,12 1 */2",
            datetime(2022, 8, 1, 0, 0),
            id="At minute 0 past hour 0 and 12 on day-of-month 1 in every 2nd month.",
        ),
        pytest.param(
            "14/15 * */2 *",
            datetime(2022, 6, 28, 19, 59),
            id="At every 15th minute from 14 through 59 on every 2nd day-of-month.",
        ),
        pytest.param(
            "* * */3 *",
            datetime(2022, 6, 30, 0, 0),
            id="At every minute on every 3rd day-of-month.",
        ),
    ],
)
def test_next_datetime_with_step_values(cron_expr, day_in_june, expected):
    it = CrontabScheduler(cron_expr, day_in_june)
    assert next(it) == expected


@pytest.mark.parametrize(
    "cron_expr",
    [
        pytest.param("-1 * * *", id="No negative minutes."),
        pytest.param("60 * * *", id="No 60 minutes."),
        pytest.param("* -2 * *", id="No negative hours."),
        pytest.param("* 24 * *", id="No 24 hours."),
        pytest.param("* * 0 *", id="No zero day."),
        pytest.param("* * -3 *", id="No negative days."),
        pytest.param("* * 32 *", id="No 32 days."),
        pytest.param("* * * 0", id="No zero month."),
        pytest.param("* * * -10", id="No negative months."),
        pytest.param("* * * 13", id="No 13 months."),
    ],
)
def test_next_datetime_with_step_values(cron_expr, day_in_june):
    with pytest.raises(ValueError):
        CrontabScheduler(cron_expr, day_in_june)


@pytest.mark.parametrize(
    "cron_expr, repeat, expected",
    [
        pytest.param(
            "* * * *", 10, datetime(2022, 6, 1, 12, 22), id="Repeat 10 times."
        ),
        pytest.param("5 10 * *", 7, datetime(2022, 6, 8, 10, 5), id="Repeat 7 times."),
        pytest.param("* * */2 *", 5, datetime(2022, 6, 2, 0, 4), id="Repeat 5 times."),
        pytest.param(
            "0 12 */2 8", 3, datetime(2022, 8, 6, 12, 0), id="Repeat 3 times."
        ),
    ],
)
def test_next_datetime_with_repeat(cron_expr, first_of_june, repeat, expected):
    it = CrontabScheduler(cron_expr, first_of_june)
    for _ in range(repeat - 1):
        next(it)
    assert next(it) == expected
