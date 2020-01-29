import pytest

from files import get_matching_files

FILES = ('bite.html commands.sh out_grepped pytest_testrun.out '
         'pytest_timings.out test_timings.py timings-template.py '
         'timings.py').split()


@pytest.mark.parametrize("filter_str, expected", [
    ('bite1', ['bite1']),
    ('Bite', ['bite1']),
    ('pybites', ['bite1']),
    ('test', ['test']),
    ('test2', ['test']),
    ('output', ['output']),
    ('o$tput', ['output']),
    ('nonsense', []),
])
def test_example_docstring(tmp_path, filter_str, expected):
    # let's create some files in tmp
    for fi in 'bite1 test output'.split():
        open(tmp_path / fi, 'a').close()
    actual = get_matching_files(tmp_path, filter_str)
    assert sorted(actual) == sorted(expected)


@pytest.mark.parametrize("filter_str, expected", [
    ('bite.html', ['bite.html']),
    ('bite.htm1', ['bite.html']),
    ('bit$.htm1', ['bite.html']),
    ('bite.txt', ['bite.html']),
    ('_timing', ['timings.py', 'test_timings.py']),
    ('commando', ['commands.sh']),
    ('pytest_testruns.out', ['pytest_testrun.out', 'pytest_timings.out']),
    ('out_greped', ['out_grepped']),
    ('nonsensical', []),
    ('commands.py', ['commands.sh']),
    ('pytest_t', ['pytest_testrun.out', 'pytest_timings.out']),
    ('timings-templates.PY', ['timings-template.py']),
])
def test_other_files(tmp_path, filter_str, expected):
    # let's create some files in tmp
    for fi in FILES:
        open(tmp_path / fi, 'a').close()
    actual = get_matching_files(tmp_path, filter_str)
    assert sorted(actual) == sorted(expected)
