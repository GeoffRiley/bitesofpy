from typing import List

import pytest
from typer.testing import CliRunner

from script import app


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()


# Test positive results
@pytest.mark.parametrize(
    "name, expected_result",
    [
        ("Geoff", "Hello Geoff!"),
        ("Carole", "Hello Carole!"),
        ("Mad Mickey", "Hello Mad Mickey!"),
    ],
)
def test_app_hello(name: str, expected_result: str, runner: CliRunner) -> None:
    result = runner.invoke(app, [name])
    assert result.exit_code == 0
    assert result.stdout.strip() == expected_result


# Test negative results . . . cannot find any negative results
# @pytest.mark.parametrize(
#     "name",
#     [
#     ],
# )
# def test_app_no_hello(name:str, runner: CliRunner) -> None:
#     result = runner.invoke(app, [name])
#     assert result.exit_code == 0  # it really shouldn't for an error!
#     assert name not in result.stdout

# Test help strings
@pytest.mark.parametrize(
    "help_message",
    [
        (
                [
                    "CLI that allows you to greet a person.",
                    "The name of the person to greet."
                ]
        ),
    ],
)
def test_app_hello_help(help_message: List[str], runner: CliRunner) -> None:
    result = runner.invoke(app, ['--help'])
    assert result.exit_code == 0
    for line in help_message:
        assert line in result.stdout
