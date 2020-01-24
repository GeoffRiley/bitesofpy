import json
from datetime import datetime
from pathlib import Path

SCORES = [10, 50, 100, 175, 250, 400, 600, 800, 1000]
BELTS = ('white yellow orange green blue brown black '
         'paneled red').split()
TMP = Path('/tmp')


def get_belts(data: str) -> dict:
    """Parsed the passed in json data:
       {"date":"5/1/2019","score":1},
       {"date":"9/13/2018","score":3},
       {"date":"10/25/2019","score":1},

       Loop through the scores in chronological order,
       determining when belts were achieved (use SCORES
       and BELTS).

       Return a dict with keys = belts, and values =
       readable dates, example entry:
       'yellow': 'January 25, 2018'
    """
    with open(data) as f:
        dat = sorted(json.load(f), key=lambda x: datetime.strptime(x["date"], "%m/%d/%Y"))
    res = {}
    total_score = 0
    belts = list(zip(SCORES, BELTS))
    belt_level = 0
    for d in dat:
        day = datetime.strptime(d['date'], "%m/%d/%Y").strftime("%B %d, %Y")
        total_score += d['score']
        if total_score >= belts[belt_level][0]:
            belt = belts[belt_level][1]
            if belt not in res:
                res[belt] = day
            belt_level += 1
            if belt_level >= len(belts):
                break
    return res
