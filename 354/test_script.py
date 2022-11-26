import pytest
import typer
from typer.testing import CliRunner

from script import main

runner = CliRunner()
app = typer.Typer()
app.command()(main)


@pytest.mark.parametrize(
    "a, b, expected_result",
    [
        ("3", "4", "The sum is 7 and c is None"),
        ("2", "5", "The sum is 7 and c is None"),
    ],
)
def test_app_sum(a, b, expected_result):
    result = runner.invoke(app, [a, b])
    assert result.exit_code == 0
    assert result.stdout.strip() == expected_result


@pytest.mark.parametrize(
    "expected_descriptions",
    [
        (
                [
                    "CLI that allows you to add two numbers",
                    "The value of the first summand",
                    "The value of the second summand",
                ]
        ),
    ],
)
def test_app_help(expected_descriptions):
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0

    for description in expected_descriptions:
        assert description in result.stdout


@pytest.mark.parametrize(
    "a, b, c, expected_result",
    [
        ("3", "4", 6, "The sum is 7 and c is smaller"),
        ("2", "5", 7, "The sum is 7 and c is not smaller"),
    ],
)
def test_app_sum_with_c(a, b, c, expected_result):
    result = runner.invoke(app, [a, b, "--c", c])
    assert result.exit_code == 0
    assert result.stdout.strip() == expected_result
