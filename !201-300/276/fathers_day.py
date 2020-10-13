from pathlib import Path
from urllib.request import urlretrieve

from dateutil.parser import parse

# get the data
tmp = Path('/tmp')
base_url = 'https://bites-data.s3.us-east-2.amazonaws.com/'

fathers_days_countries = tmp / 'fathers-day-countries.txt'
fathers_days_recurring = tmp / 'fathers-day-recurring.txt'

for file_ in (fathers_days_countries, fathers_days_recurring):
    if not file_.exists():
        urlretrieve(base_url + file_.name, file_)


def _parse_father_days_per_country(year, filename=fathers_days_countries):
    """Helper to parse fathers_days_countries"""
    result = {}
    with open(filename) as f:
        for line in f.read().splitlines(keepends=False):
            if line.startswith('#'):
                continue
            if line.startswith('*'):
                countries = [cnt.strip() if not cnt.startswith(' and') else cnt[4:].strip() for cnt in
                             line[1:].split(',')]
                continue
            if line.startswith(str(year)):
                result[line.split(':')[1].strip()] = countries
    return result


def _parse_recurring_father_days(filename=fathers_days_recurring):
    """Helper to parse fathers_days_recurring"""
    result = {}
    with open(filename) as f:
        for line in f.read().splitlines(keepends=False):
            if line.startswith('#') or len(line.strip()) == 0:
                continue
            if line.startswith('*'):
                date_ = line[1:].strip()
                result[date_] = []
                continue
            result[date_].append(line.strip())
    return result


def get_father_days(year=2020):
    """Returns a dictionary of keys = dates and values = lists
       of countries that celebrate Father's day that date

       Consider using the the 2 _parse* helpers.
    """
    result = _parse_recurring_father_days()
    for d, c in _parse_father_days_per_country(year).items():
        if d in result:
            result[d].extend(c)
        else:
            result[d] = c
    return result


def generate_father_day_planning(father_days=None):
    """Prints all father days in order, example in tests and
       Bite description
    """
    if father_days is None:
        father_days = get_father_days()

    for d, c in sorted(father_days.items(), key=lambda x: parse(x[0])):
        print(d)
        print('- ' + '\n- '.join(c))
        print()
