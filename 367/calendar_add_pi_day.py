import calendar
from typing import List, Tuple

PI_DAY_DESC = 'π Day'
PI_DAY_MONTH = 3
PI_DAY_DAY = 14
PI_DAY_DEFAULT_DATE_LIST = [(PI_DAY_MONTH, PI_DAY_DAY, PI_DAY_DESC)]


class InvalidYear(Exception):
    pass


def create_calendar(year: int, dates: List[Tuple[int, int, str]]) -> None:
    """Accept a list of tuples with a month, a day and a description. They will not necessarily come in date order.
    Print out a calendar of each month with one of the dates, followed by a line for each of the events in that month
    showing day of the week, day of the month then the event description, sorted by day of the week and then
    day of the month.
    Add Pie Day (3/14) as a date whether it is entered or not.
    If the year passed into the function is  not valid (an integer between 1 and 9999) raise an InvalidYear exception

    An example will make this much easier!
    create_calendar(2000, [(1, 25, "My birthday"),
                       (1, 27, "e-Day"),
                       (1, 8, "Earth Rotation Day"),
                       (4, 12, "Grilled Cheese Day"),
                       (1, 20, "Penguin Awareness Day"),
                       ])


    should print-

        January 2000
    Su Mo Tu We Th Fr Sa
                       1
     2  3  4  5  6  7  8
     9 10 11 12 13 14 15
    16 17 18 19 20 21 22
    23 24 25 26 27 28 29
    30 31
    Tuesday 25: My birthday
    Thursday 20: Penguin Awareness Day
    Thursday 27: e-Day
    Saturday 8: Earth Rotation Day

         March 2000
    Su Mo Tu We Th Fr Sa
              1  2  3  4
     5  6  7  8  9 10 11
    12 13 14 15 16 17 18
    19 20 21 22 23 24 25
    26 27 28 29 30 31
    Tuesday 14: π Day

             April 2000
    Su Mo Tu We Th Fr Sa
                       1
     2  3  4  5  6  7  8
     9 10 11 12 13 14 15
    16 17 18 19 20 21 22
    23 24 25 26 27 28 29
    30
    Wednesday: Grilled Cheese Day

    :param year:
    :type year: int
    :param dates: 
    :type dates: list of tuples, each of which has a month(int), day(int) and description (str)
    :return: None
    """
    if not isinstance(year, int) or not (1 < year < 9999):
        raise InvalidYear

    cal = calendar.TextCalendar(firstweekday=calendar.SUNDAY)
    s_dates = sorted(
        [(mn, calendar.weekday(year, mn, dt), dt, desc) for mn, dt, desc in dates + PI_DAY_DEFAULT_DATE_LIST])

    mm = 0
    this_month = []
    for mn, dow, dt, desc in s_dates:
        if mn != mm:
            if mm > 0:
                print('')
            cal.prmonth(year, mn)
            mm = mn
        print(f'{calendar.day_name[dow]}: {desc}')

    print('')
