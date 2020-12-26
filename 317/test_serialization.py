from datetime import date
import time
from typing import NamedTuple

from serialization import (download_pickle_file,
                           deserialize,
                           serialize,
                           TMP,
                           MovieRented)


class Bite(NamedTuple):
    title: str
    number: int
    level: str


def test_deserialize_movie_rented_data():
    download_pickle_file()
    expected = [
        MovieRented('Mad Max Fury Road', 4, date(2020, 12, 1)),
        MovieRented('Mad Max Fury Road', 4, date(2020, 12, 17)),
        MovieRented('Die Hard', 4, date(2020, 12, 3)),
        MovieRented('Tenet', 20, date(2020, 12, 1)),
        MovieRented('Breach', 7, date(2020, 11, 17)),
        MovieRented('Spider-Man', 12, date(2020, 12, 28)),
        MovieRented('Sonic', 10, date(2020, 11, 4))
    ]
    actual = deserialize()
    assert actual == expected


def test_serialize_and_deserialize_other_data():
    data = [
        Bite('Sum of Numbers', 1, 'Beginner'),
        Bite('Regex Fun', 2, 'Advanced'),
    ]
    pkl_file = TMP / str(int(time.time()))
    serialize(pkl_file, data=data)
    actual = deserialize(pkl_file)
    expected = data
    assert actual == expected
