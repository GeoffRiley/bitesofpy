from typing import List

import pytest
from typer.testing import CliRunner

from script import app


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()


@pytest.mark.parametrize(
    "a, b, expected_result",
    [
        ("3", "4", "The sum is 7"),
        ("2", "5", "The sum is 7"),
    ],
)
def test_app_sum(a: str, b: str, expected_result: str, runner: CliRunner) -> None:
    result = runner.invoke(app, ["sum", a, b])
    assert result.exit_code == 0
    assert result.stdout.strip() == expected_result


@pytest.mark.parametrize(
    "expected_descriptions",
    [
        (
                [
                    "Command that allows you to add two numbers.",
                    "The value of the first summand",
                    "The value of the second summand",
                ]
        ),
    ],
)
def test_app_sum_help(expected_descriptions: List[str], runner: CliRunner) -> None:
    result = runner.invoke(app, ["sum", "--help"])
    assert result.exit_code == 0
    for description in expected_descriptions:
        assert description in result.stdout


@pytest.mark.parametrize(
    "c, d, expected_result",
    [
        ("5", "4", "d=4 is not greater than c=5"),
        ("2", "7", "d=7 is greater than c=2"),
    ],
)
def test_app_compare(c: str, d: str, expected_result: str, runner: CliRunner) -> None:
    result = runner.invoke(app, ["compare", c, d])
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
def test_app_compare_help(expected_descriptions: List[str], runner: CliRunner) -> None:
    result = runner.invoke(app, ["compare", "--help"])
    assert result.exit_code == 0
    for description in expected_descriptions:
        assert description in result.stdout
