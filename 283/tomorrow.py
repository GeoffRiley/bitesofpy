from datetime import date, timedelta, datetime


def tomorrow(d: date = None) -> date:
    if not d:
        d = datetime.today().date()

    return d + timedelta(days=1)
