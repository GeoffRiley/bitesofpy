import pytest

from calendar_add_pi_day import InvalidYear
from calendar_add_pi_day import create_calendar


@pytest.mark.parametrize("year, dates, expected", [
    (2000, [],
     """     March 2000
Su Mo Tu We Th Fr Sa
          1  2  3  4
 5  6  7  8  9 10 11
12 13 14 15 16 17 18
19 20 21 22 23 24 25
26 27 28 29 30 31
Tuesday: π Day

"""),
    (2015, [(1, 25, "My birthday"),
            (1, 27, "e-Day"),
            (1, 8, "Earth Rotation Day"),
            (4, 12, "Grilled Cheese Day"),
            (1, 20, "Penguin Awareness Day"),
            ],
     """    January 2015
Su Mo Tu We Th Fr Sa
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 19 20 21 22 23 24
25 26 27 28 29 30 31
Tuesday: Penguin Awareness Day
Tuesday: e-Day
Thursday: Earth Rotation Day
Sunday: My birthday

     March 2015
Su Mo Tu We Th Fr Sa
 1  2  3  4  5  6  7
 8  9 10 11 12 13 14
15 16 17 18 19 20 21
22 23 24 25 26 27 28
29 30 31
Saturday: π Day

     April 2015
Su Mo Tu We Th Fr Sa
          1  2  3  4
 5  6  7  8  9 10 11
12 13 14 15 16 17 18
19 20 21 22 23 24 25
26 27 28 29 30
Sunday: Grilled Cheese Day

"""),
    (2000, [(2, 27, 'No Brainer Day')],
     """   February 2000
Su Mo Tu We Th Fr Sa
       1  2  3  4  5
 6  7  8  9 10 11 12
13 14 15 16 17 18 19
20 21 22 23 24 25 26
27 28 29
Sunday: No Brainer Day

     March 2000
Su Mo Tu We Th Fr Sa
          1  2  3  4
 5  6  7  8  9 10 11
12 13 14 15 16 17 18
19 20 21 22 23 24 25
26 27 28 29 30 31
Tuesday: π Day

"""),
    (2023, [(3, 23, 'Puppy Day'), (3, 20, 'World Storytelling Day')],
     """     March 2023
Su Mo Tu We Th Fr Sa
          1  2  3  4
 5  6  7  8  9 10 11
12 13 14 15 16 17 18
19 20 21 22 23 24 25
26 27 28 29 30 31
Monday: World Storytelling Day
Tuesday: π Day
Thursday: Puppy Day

""")
])
def test_calendar(capsys, year, dates, expected):
    create_calendar(year, dates)
    captured = capsys.readouterr()
    assert captured.out == expected


@pytest.mark.parametrize("year", [-1, 0, 10000, None, 1.2, "3", False])
def test_invalid_year(year):
    with pytest.raises(InvalidYear):
        create_calendar(year, [])
