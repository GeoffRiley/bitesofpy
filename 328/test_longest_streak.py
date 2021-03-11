import sys
from datetime import date
from urllib.request import urlretrieve
from zipfile import ZipFile

import pytest

from longest_streak import TMP, longest_streak, MY_TZ, UTC

S3 = "https://bites-data.s3.us-east-2.amazonaws.com"
RESULTS = [
    (date(2019, 10, 10), date(2019, 10, 11)),
    (date(2019, 10, 13), date(2019, 10, 14)),
    None,
    (date(2019, 10, 1), date(2019, 10, 1)),
]

RESULTS_UTC = [
    (date(2019, 10, 9), date(2019, 10, 13)),
    (date(2019, 10, 9), date(2019, 10, 14)),
    None,
    (date(2019, 10, 2), date(2019, 10, 2)),
]
PATHS = [TMP / f"test{x}.json" for x in range(1, 5)]

sys.path.append(TMP)


@pytest.fixture(scope="module")
def download_test_files():
    data_zipfile = 'bite328_test_data.zip'
    urlretrieve(f'{S3}/{data_zipfile}', TMP / data_zipfile)
    ZipFile(TMP / data_zipfile).extractall(TMP)


@pytest.mark.parametrize("argument, expected",
                         zip(PATHS, RESULTS))
def test_longest_streak_easterntz(argument, expected, download_test_files):
    assert longest_streak(argument, MY_TZ) == expected


@pytest.mark.parametrize("argument, expected",
                         zip(PATHS, RESULTS_UTC))
def test_longest_streak_utc(argument, expected, download_test_files):
    assert longest_streak(argument, UTC) == expected
