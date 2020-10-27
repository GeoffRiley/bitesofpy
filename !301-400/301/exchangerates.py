import datetime as dt
import json
import os
from collections import OrderedDict
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Union, Any
from urllib.request import urlretrieve

URL = "https://bites-data.s3.us-east-2.amazonaws.com/exchangerates.json"
TMP = Path(os.getenv("TMP", "/tmp"))
RATES_FILE = TMP / "exchangerates.json"
DATAFILE: Union[Any, None] = None

if not RATES_FILE.exists():
    urlretrieve(URL, RATES_FILE)


def str_to_date(d: Union[str, date]) -> date:
    """
    Defensive conversion of a string to a date
    If a date object is passed, then it is returned untouched
    """
    return d if isinstance(d, date) else dt.datetime.strptime(d, '%Y-%m-%d').date()


def load_data_file() -> None:
    """
    Loads the json file into memory and converts date strings
    into date objects; also sorts the rates into date order
    If the datafile has already been loaded, this routine does nothing
    """
    global DATAFILE
    if DATAFILE:
        return
    with open(RATES_FILE, 'rt') as f:
        DATAFILE = json.load(f)
    DATAFILE['start_at'] = str_to_date(DATAFILE['start_at'])
    DATAFILE['end_at'] = str_to_date(DATAFILE['end_at'])
    rates = {str_to_date(d): v for d, v in DATAFILE['rates'].items()}
    DATAFILE['rates'] = OrderedDict(sorted(rates.items()))


def get_all_days(start_date: date, end_date: date) -> List[date]:
    load_data_file()
    if start_date < DATAFILE['start_at'] or end_date > DATAFILE['end_at']:
        raise ValueError('Requested data outside available range')
    return [
        start_date + timedelta(days=d)
        for d in range((end_date - start_date).days + 1)
    ]


def rate_date_for(d: date, rate_dates: set) -> date:
    """
    Seek out the date that the exchange was most recently open
    on or before the given date
    """
    while d > min(rate_dates) and d not in rate_dates:
        d = d - timedelta(days=1)
    return d


def match_daily_rates(
        start: date, end: date, daily_rates: dict
) -> Dict[date, date]:
    res = OrderedDict()
    key_t = set(type(k) for k in daily_rates.keys())
    if str in key_t:
        rate_dates = set(str_to_date(d) for d in daily_rates.keys())
    else:
        rate_dates = set(daily_rates.keys())
    for d in get_all_days(start, end):
        res[d] = rate_date_for(d, rate_dates)
    return res


def exchange_rates(
        start_date: str = "2020-01-01", end_date: str = "2020-09-01"
) -> Dict[date, dict]:
    rates = DATAFILE['rates']
    days = match_daily_rates(
        str_to_date(start_date),
        str_to_date(end_date),
        rates)
    res = dict()
    for k, v in days.items():
        res[k] = {
            'Base Date': v,
            'USD': rates[v]['USD'],
            'GBP': rates[v]['GBP']
        }
    return res
