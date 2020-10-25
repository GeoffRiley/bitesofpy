import filecmp
from urllib.request import urlretrieve

import pytest
from get_my_code import get_passing_code, url, tmp


@pytest.mark.parametrize('actual_filename, expected_filename', [
    ('Bite01.py', 'Bite01_Expected.py'),
    ('Bite02.py', 'Bite02_Expected.py')
])
def test_compare_files(actual_filename, expected_filename):
    actual = tmp / actual_filename
    expected = tmp / expected_filename
    get_passing_code()
    urlretrieve(url.format(filename=expected_filename),
                expected)
    assert filecmp.cmp(actual, expected)
