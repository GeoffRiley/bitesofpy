import pytest

from timings import timings_log, get_bite_with_fastest_avg_test


@pytest.fixture(scope='module')
def timings():
    with open(timings_log) as f:
        return f.readlines()


@pytest.mark.parametrize("rows, expected_bites", [
    (50, '121'),
    (100, '169'),
    (150, '169'),
    (200, '46'),
    (250, ('60', '87')),
])
def test_get_bite_with_fastest_avg_test(rows, expected_bites, timings):
    actual = str(get_bite_with_fastest_avg_test(timings[:rows]))
    if type(expected_bites) == tuple:
        assert actual in expected_bites
    else:
        assert actual == expected_bites
