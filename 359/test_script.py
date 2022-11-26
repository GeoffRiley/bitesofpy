from typing import List

import pytest
from typer.testing import CliRunner

from script import app


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()


#####
# Tests for **subtract** function
#

@pytest.mark.parametrize(
    "a, b, expect_result",
    [
        ("10", "5", "The delta is 5"),
        ("10", "1", "The delta is 9"),
    ],
)
def test_app_subtract_positive_results(a: str, b: str, expect_result: str, runner: CliRunner) -> None:
    result = runner.invoke(app, ['subtract', a, b])
    assert result.exit_code == 0
    assert result.stdout.strip() == expect_result


@pytest.mark.parametrize(
    "a, b, expect_result",
    [
        ("5", "10", "The delta is -5"),
        ("1", "10", "The delta is -9"),
    ],
)
def test_app_subtract_negative_results(a: str, b: str, expect_result: str, runner: CliRunner) -> None:
    result = runner.invoke(app, ['subtract', a, b])
    assert result.exit_code == 0
    assert result.stdout.strip() == expect_result


@pytest.mark.parametrize(
    "expected_help",
    [
        (
                [
                    # Yes, the code being tested says 'add' instead of 'subtract',
                    # and 'summand' instead of 'minuend' and 'subtrahend'!!
                    # (Anyone who isn't into maths understand these terms?)
                    'Command that allows you to add two numbers.',
                    'The value of the first summand',
                    'The value of the second summand',
                ]
        )
    ],
)
def test_app_subtract_help(expected_help: List[str], runner: CliRunner) -> None:
    result = runner.invoke(app, ['subtract', '--help'])
    assert result.exit_code == 0
    for line in expected_help:
        assert line in result.stdout


#####
# Tests for **compare** function
#

@pytest.mark.parametrize(
    "c, d, expected_result",
    [
        ("1", "2", "d=2 is greater than c=1"),
        ("3", "2", "d=2 is not greater than c=3"),
        ("0", "0", "d=0 is not greater than c=0"),
        # -10 makes typer think we're specifying an option of '-1'
        # ("-10", "10", "d=10 is greater than c=-10"),
    ],
)
def test_app_compare_values(c: str, d: str, expected_result: str, runner: CliRunner) -> None:
    result = runner.invoke(app, ['compare', c, d])
    assert result.exit_code == 0
    assert result.stdout.strip() == expected_result


@pytest.mark.parametrize(
    "expected_help",
    [
        (
                [
                    'Command that checks whether a number d is greater than a number c.',
                    'First number to compare against.',
                    'Second number that is compared against first number.'
                ]
        )
    ],
)
def test_app_compare_help(expected_help: List[str], runner: CliRunner) -> None:
    result = runner.invoke(app, ['compare', '--help'])
    assert result.exit_code == 0
    for line in expected_help:
        assert line in result.stdout
