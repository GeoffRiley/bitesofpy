import json
import os
from collections import defaultdict
from datetime import date, tzinfo
from pathlib import Path
from typing import Tuple, Optional

from dateutil.parser import parse
from dateutil.tz import gettz

DATA_FILE_NAME = "test1.json"
TMP = Path(os.getenv("TMP", "/tmp"))
DATA_PATH = TMP / DATA_FILE_NAME
MY_TZ = gettz("America/New York")
UTC = gettz("UTC")


def longest_streak(
        data_file: Path = DATA_PATH, my_tz: Optional[tzinfo] = MY_TZ
) -> Optional[Tuple[date, date]]:
    """Retrieve datetime strings of passed commits and calculate the longest
    streak from the user's data

    Note: The datetime strings will need to be used to create aware datetime objects

    All datetimes are in UTC, and the timezone of the user is part of the context
    for calculating a streak. Ex: 2019-10-14 01:58:48.129585+00:00 is 2019-10-13 in
    New York City. You will need to convert datetimes from UTC into the supplied timezone.

    The tests show an example of how a streak can change based on the timezone used.

    If the dataset has two or more streaks of the same length as longest, provide
    only the most recent streak.

    Return a tuple containing start and end date for the longest streak
    or None
    """
    with open(data_file) as f:
        data = json.load(f)

    # Use a set to automatically discount duplicated dates!
    diary = set()
    for bite in data['commits']:
        if bite['passed']:
            diary.add(parse(bite['date']).astimezone(my_tz).toordinal())

    if not diary:
        return None

    diary = sorted(diary)
    runs = defaultdict(set)
    current_start = diary[0]
    current_run = 0
    for current_date in diary:
        if current_date == current_start + current_run:
            current_run += 1
            continue
        runs[current_run].add(current_start)
        current_start = current_date
        current_run = 1
    if current_run > 0:
        runs[current_run].add(current_start)
    long_run = max(runs.keys())
    long_start = runs[long_run].pop()

    return date.fromordinal(long_start), date.fromordinal(long_start + long_run - 1)


if __name__ == "__main__":
    streak = longest_streak()
    print(f"My longest streak went from {streak[0]} through {streak[1]}")
    print(f"The streak lasted {(streak[1] - streak[0]).days + 1} days")
