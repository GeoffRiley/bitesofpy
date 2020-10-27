import json
from datetime import date

import pytest
from exchangerates import RATES_FILE, exchange_rates, get_all_days, match_daily_rates


@pytest.fixture(scope="session")
def exchange_rates_result():
    return exchange_rates()


@pytest.fixture(scope="session")
def matching_result():
    start = date(2020, 1, 1)
    end = date(2020, 9, 1)
    daily_rates = json.loads(RATES_FILE.read_text())["rates"]
    return match_daily_rates(start, end, daily_rates)


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (date(2020, 1, 1), date(2020, 1, 31), 31),
        (date(2020, 1, 14), date(2020, 1, 29), 16),
        (date(2020, 4, 12), date(2020, 4, 14), 3),
    ],
)
def test_get_all_days(start, end, expected):
    actual = get_all_days(start, end)
    assert len(actual) == expected

    assert isinstance(actual[0], date)
    assert isinstance(actual[-1], date)

    assert actual[0] == start
    assert actual[-1] == end


@pytest.mark.parametrize(
    "date, expected",
    [
        (date(2020, 1, 18), date(2020, 1, 17)),
        (date(2020, 2, 2), date(2020, 1, 31)),
        (date(2020, 5, 3), date(2020, 4, 30)),
        (date(2020, 8, 15), date(2020, 8, 14)),
    ],
)
def test_match_daily_rates(date, expected, matching_result):
    actual = matching_result
    assert actual[date] == expected


@pytest.mark.parametrize(
    "testdate, expected",
    [
        (
                date(2020, 7, 16),
                {"Base Date": date(2020, 7, 16), "GBP": 0.90875, "USD": 1.1414},
        ),
        (
                date(2020, 7, 17),
                {"Base Date": date(2020, 7, 17), "GBP": 0.91078, "USD": 1.1428},
        ),
        (
                date(2020, 7, 18),
                {"Base Date": date(2020, 7, 17), "GBP": 0.91078, "USD": 1.1428},
        ),
    ],
)
def test_exchange_rates_sample(testdate, expected, exchange_rates_result):
    actual = exchange_rates_result

    assert actual[testdate]["Base Date"] == expected["Base Date"]
    assert actual[testdate]["GBP"] == expected["GBP"]
    assert actual[testdate]["USD"] == expected["USD"]


def test_exchange_rates_all_dates(exchange_rates_result):
    assert len(exchange_rates_result) == 245


def test_exchange_rates_order(exchange_rates_result):
    actual = list(exchange_rates_result.keys())
    expected = sorted(exchange_rates_result.keys())

    assert actual == expected


def test_exchange_rates_validate_start():
    with pytest.raises(ValueError):
        exchange_rates(start_date="1950-01-01")


def test_exchange_rates_validate_end():
    with pytest.raises(ValueError):
        exchange_rates(end_date="2050-01-01")
