import pytest
from typer.testing import CliRunner

from script import app

runner = CliRunner()


@pytest.mark.parametrize(
    "verbose, a, b, expected_result",
    [
        (False, "3", "4", "7"),
        (False, "2", "5", "7"),
        (True, "3", "4", "Will write verbose output\nThe sum is 7"),
        (True, "2", "5", "Will write verbose output\nThe sum is 7"),
    ],
)
def test_app_sum(verbose, a, b, expected_result):
    if verbose:
        result = runner.invoke(app, ["algorithms", "--verbose", "sum", a, b])
    else:
        result = runner.invoke(app, ["algorithms", "sum", a, b])

    assert result.exit_code == 0
    assert result.stdout.strip() == expected_result


@pytest.mark.parametrize(
    "expected_descriptions",
    [
        (
                [
                    "Command that allows you to add two numbers",
                    "The value of the first summand",
                    "The value of the second summand",
                ]
        ),
    ],
)
def test_app_sum_help(expected_descriptions):
    result = runner.invoke(app, ["algorithms", "sum", "--help"])
    assert result.exit_code == 0
    for description in expected_descriptions:
        assert description in result.stdout


@pytest.mark.parametrize(
    "verbose, c, d, expected_result",
    [
        (False, "5", "4", "d > c: False"),
        (False, "2", "7", "d > c: True"),
        (True, "5", "4", "Will write verbose output\nd=4 is not greater than c=5"),
        (True, "2", "7", "Will write verbose output\nd=7 is greater than c=2"),
    ],
)
def test_app_compare(verbose, c, d, expected_result):
    if verbose:
        result = runner.invoke(app, ["comparisons", "--verbose", "compare", c, d])
    else:
        result = runner.invoke(app, ["comparisons", "compare", c, d])

    assert result.exit_code == 0
    assert result.stdout.strip() == expected_result


@pytest.mark.parametrize(
    "expected_descriptions",
    [
        (
                [
                    "Command that checks whether a number d is greater than a number c.",
                    "First number to compare against.",
                    "Second number that is compared against first number.",
                ]
        ),
    ],
)
def test_app_compare_help(expected_descriptions):
    result = runner.invoke(app, ["comparisons", "compare", "--help"])
    assert result.exit_code == 0
    for description in expected_descriptions:
        assert description in result.stdout
