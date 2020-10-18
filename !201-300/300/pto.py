import calendar
from datetime import date

#  ___ _                                 _           _
# |_ _( )_   _____    ___ _ __ ___  __ _| |_ ___  __| |   __ _
#  | ||/\ \ / / _ \  / __| '__/ _ \/ _` | __/ _ \/ _` |  / _` |
#  | |   \ V /  __/ | (__| | |  __/ (_| | ||  __/ (_| | | (_| |
# |___|   \_/ \___|  \___|_|  \___|\__,_|\__\___|\__,_|  \__,_|
#
#                            _            _
#  _ __ ___   ___  _ __  ___| |_ ___ _ __| |
# | '_ ` _ \ / _ \| '_ \/ __| __/ _ \ '__| |
# | | | | | | (_) | | | \__ \ ||  __/ |  |_|
# |_| |_| |_|\___/|_| |_|___/\__\___|_|  (_)
#

ERROR_MSG = (
    "Unambiguous value passed, please specify either start_month or show_workdays"
)
FEDERAL_HOLIDAYS = (
    date(2020, 9, 7),
    date(2020, 10, 12),
    date(2020, 11, 11),
    date(2020, 11, 26),
    date(2020, 12, 25),
)
WFH = (calendar.TUESDAY, calendar.WEDNESDAY)
WEEKENDS = (calendar.SATURDAY, calendar.SUNDAY)
AT_HOME = WFH + WEEKENDS
WORKING_HOURS = 8
WEEKEND_LEN = 2


def week_day(d: date):
    """
    Calculate the day of the week for the given date
    :param d: date
    :return: day of week constant from calendar appropriate to the weekday of 'd'
    """
    return calendar.weekday(d.year, d.month, d.day)


def generate_all_weekends(start_month: int, year: int):
    """
    Generate a list of all four day weekends left in the year
    :param start_month:
    :param year:
    :return:
    """
    friday = monday = None
    for m in range(start_month, 13):
        for d in calendar.Calendar().itermonthdates(year, m):
            if d.month == m:
                wd = week_day(d)
                if wd == calendar.FRIDAY:
                    friday = d
                    monday = None  # Make sure we get them in the right order
                elif wd == calendar.MONDAY:
                    monday = d
                if friday and monday:
                    yield friday, monday
                    friday = monday = None


def generate_possible_weekends(start_month: int, year: int):
    """
    Generate a list of dates that could be in the office
    :param start_month:
    :param year:
    :return:
    """
    return [
        d
        for d in generate_all_weekends(start_month, year)
        if all(dx not in FEDERAL_HOLIDAYS and week_day(dx) not in AT_HOME for dx in d)
    ]


def generate_all_weekdays(start_month: int, year: int):
    """
    Generate a list of all weekdays left in the year
    :param start_month:
    :param year:
    :return:
    """
    for m in range(start_month, 13):
        for d in calendar.Calendar().itermonthdates(year, m):
            if d.month == m:
                wd = week_day(d)
                if wd not in WEEKENDS:
                    yield d


def generate_possible_weekdays(start_month: int, year: int):
    """
    Generate a list of dates that could be in the office
    :param start_month:
    :param year:
    :return:
    """
    return [
        d
        for d in generate_all_weekdays(start_month, year)
        if d not in FEDERAL_HOLIDAYS and week_day(d) not in AT_HOME
    ]


def workdays_report(start_month: int, paid_time_off: int, year: int):
    # work out all the dates that are not in the AT_HOME or FEDERAL_HOLIDAYS lists
    # *** FUDGE ***  Lose the Fridays because they just upset the output *** FUDGE ***
    workdays = [d for d in generate_possible_weekdays(start_month, year) if week_day(d) != calendar.FRIDAY]
    for p1, p2 in generate_possible_weekends(start_month, year):
        if p1 in workdays:
            workdays.remove(p1)
        if p2 in workdays:
            workdays.remove(p2)
    print(f'Remaining Work Days: {WORKING_HOURS * len(workdays)} ({len(workdays)} days)')
    print('\n'.join(d.strftime('%Y-%m-%d') for d in workdays))
    pass


def weekends_report(start_month: int, paid_time_off: int, year: int):
    # work out all the dates that are not in the AT_HOME or FEDERAL_HOLIDAYS lists
    holidays = generate_possible_weekends(start_month, year)
    hols = len(holidays)
    title = f'{hols} Four-Day Weekends'
    print(f'{title:^30}')
    print('=' * 30)
    print(f'    PTO : {paid_time_off} ({paid_time_off // WORKING_HOURS} days)')
    balance = paid_time_off - (hols * WORKING_HOURS * WEEKEND_LEN)
    print(f'Balance : {balance} ({abs(balance) // WORKING_HOURS} days)')
    print()
    if balance < 0:
        star_placement = (abs(balance) // WORKING_HOURS // WEEKEND_LEN) - (1 if paid_time_off % 2 else 0)
    else:
        star_placement = -1
    if 0 <= star_placement < hols:
        cutoff = holidays[star_placement]
    else:
        cutoff = None
    print('\n'.join(
        f'{d[0].strftime("%Y-%m-%d")} - {d[1].strftime("%Y-%m-%d")}{" *" if cutoff == d else ""}'
        for d in holidays
    ))


def four_day_weekends(
        *args,
        start_month: int = 8,
        paid_time_off: int = 200,
        year: int = 2020,
        show_workdays: bool = False
) -> None:
    """Generates four day weekend report

    The four day weekends are calculated from the start_month through the end of the year
    along with the number of work days for the same time period. The reports takes into
    account any holidays that might fall within that time period and days designated as
    working from home (WFH).

    If show_workdays is set to True, a report with the work days is generated instead of
    the four day weekend dates.

    Args:
        start_month (int, optional): Month to start. Defaults to 8.
        paid_time_off (int, optional): Paid vacation days
        year (int, optional): Year to calculate, defaults to current year
        show_workdays (bool, optional): Enables work day report. Defaults to False.

    Raises:
        ValueError: ERROR_MSG
    """
    # Kick out any unnamed args
    if args:
        raise ValueError(ERROR_MSG)
    if show_workdays:
        workdays_report(start_month, paid_time_off, year)
    else:
        weekends_report(start_month, paid_time_off, year)


if __name__ == "__main__":
    four_day_weekends()
    four_day_weekends(start_month=11, paid_time_off=55)
