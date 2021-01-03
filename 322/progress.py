from datetime import datetime
from typing import Union


def ontrack_reading(books_goal: int, books_read: Union[int, float],
                    day_of_year: int = None) -> bool:
    if day_of_year is None:
        day_of_year = datetime.today().timetuple().tm_yday
    return books_read >= books_goal / 365 * day_of_year
