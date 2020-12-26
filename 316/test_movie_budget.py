from datetime import date

import pytest

from movie_budget import rent_or_stream, MovieRented


@pytest.mark.parametrize("arg, expected", [
    ([MovieRented('Mad Max Fury Road', 4, date(2020, 12, 1))],
     {"2020-12": "rent"}),
    ([MovieRented('Mad Max Fury Road', 4, date(2020, 12, 17)),
      MovieRented('Die Hard', 4, date(2020, 12, 3)),
      MovieRented('Wonder Woman', 4, date(2020, 12, 28))],
     {"2020-12": "rent"}),
    ([MovieRented('Tenet', 20, date(2020, 12, 1))],
     {"2020-12": "stream"}),
    ([MovieRented('Breach', 7, date(2020, 11, 17)),
      MovieRented('Die Hard', 4, date(2020, 11, 3)),
      MovieRented('Tenet', 20, date(2020, 12, 28))],
     {"2020-11": "rent", "2020-12": 'stream'}),
    ([MovieRented('Spider-Man', 12, date(2020, 12, 28)),
      MovieRented('Sonic', 10, date(2020, 11, 4)),
      MovieRented('Die Hard', 3, date(2020, 11, 3))],
     {"2020-11": "stream", "2020-12": 'rent'}),
])
def test_rent_or_stream(arg, expected):
    assert rent_or_stream(arg) == expected
