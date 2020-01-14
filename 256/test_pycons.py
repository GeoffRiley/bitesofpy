import datetime

import pytest
from pycons import (get_pycon_events, filter_pycons,
                    get_continent)


@pytest.fixture(scope="session")
def pycon_events():
    events = get_pycon_events()
    return events


@pytest.fixture(scope="session")
def filtered_pycons(pycon_events):
    filtered = filter_pycons(pycon_events)
    return filtered


def test_get_pycon_events_number(pycon_events):
    assert len(pycon_events) == 21


def test_get_pycon_events_cities(pycon_events):
    actual = {event.city for event in pycon_events}
    expected = {
        "Accra", "Belgrade", "Belgrade", "Berlin",
        "Bratislava", "Cardiff", "Cleveland, OH", "Dublin",
        "Florence", "Hyderabad", "Jakarta", "Johannesburg",
        "Makati", "Munich", "Nairobi", "Odessa",
        "Ostrava", "Puerto Vallarta", "Sydney",
        "Taipei", "Toronto",
    }
    assert actual == expected


def test_get_pycon_events_dates(pycon_events):
    assert all(
        isinstance(event.start_date, datetime.datetime)
        for event in pycon_events
    )
    assert all(isinstance(event.end_date, datetime.datetime)
               for event in pycon_events)


def test_filter_pycons_number(filtered_pycons):
    actual = len(filtered_pycons)
    expected = 9
    assert actual == expected


def test_filter_pycons_cities(filtered_pycons):
    actual = {event.city for event in filtered_pycons}
    expected = {
        "Belgrade", "Berlin", "Bratislava", "Cardiff",
        "Dublin", "Florence", "Munich", "Odessa",
        "Ostrava",
    }
    assert actual == expected


def test_filter_pycons_dates(filtered_pycons):
    assert all(
        isinstance(event.start_date, datetime.datetime)
        for event in filtered_pycons
    )
    assert all(
        isinstance(event.end_date, datetime.datetime)
        for event in filtered_pycons
    )


def test_filter_pycons_year(filtered_pycons):
    actual = {pycon.start_date.year for pycon in filtered_pycons}
    expected = {2019}
    assert actual == expected


def test_filter_pycons_continent(filtered_pycons):
    actual = {get_continent(pycon.country) for pycon in filtered_pycons}
    expected = {"Europe"}
    assert actual == expected
