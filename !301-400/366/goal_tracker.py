from datetime import date
from typing import Tuple


def goal_tracker(desc: str, annual_target: int, current_score: int, score_date: Tuple[int, int, int]):
    """Return a string determining whether a goal is on track
    by calculating the current target and comparing it with the current achievement.
    The function assumes the goal is to be achieved in a calendar year. Think New Year's Resolution :)
    """
    year, *_ = score_date

    # try:  # Ignore exceptions!!
    dt = date(*score_date)
    eoy = date(year, 12, 31)
    # except (ValueError, TypeError):
    #     raise

    day_of_year = dt.timetuple().tm_yday
    days_in_year = eoy.timetuple().tm_yday
    todays_target = int((annual_target / days_in_year) * day_of_year)

    date_diff = current_score - todays_target

    if date_diff < 0:
        s1 = 'You have some catching up to do!'
        s2 = 'behind'
    else:
        s1 = f'Congratulations! You are on track with your {desc} goal.'
        s2 = 'ahead'

    return f'{s1} The target for {dt.strftime("%Y-%m-%d")} is ' \
           f'{todays_target:,} {desc} and you are {abs(date_diff)} {s2}.'
