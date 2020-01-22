import re
from pathlib import Path
from urllib.request import urlretrieve

tmp = Path('/tmp')
timings_log = tmp / 'pytest_timings.out'
if not timings_log.exists():
    urlretrieve(
        'https://bites-data.s3.us-east-2.amazonaws.com/pytest_timings.out',
        timings_log
    )


def get_bite_with_fastest_avg_test(timings: list) -> str:
    """Return the bite which has the fastest average time per test"""
    timing_list = []
    for line in timings:
        if line is not None and len(line) > 0:
            bite, count, ticks = re.search(r'(\d+) =* (\d+|no tests) \w+(?:, \d+ \w+)? in ([\d.]+)', line).groups()
            if count != 'no tests':
                timing_list.append([float(ticks) / float(count), bite])
    return sorted(timing_list)[0][1]
