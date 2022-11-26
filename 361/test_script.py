import pytest
from typer.testing import CliRunner

from script import app

runner = CliRunner()


@pytest.mark.parametrize(
    "expected",
    [
        (
                [
                    "┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓",
                    "┃ Name   ┃ Favorite Tool/Framework ┃",
                    "┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━┩",
                    "│ Bob    │ Vim                     │",
                    "│ Julian │ Flask                   │",
                    "│ Robin  │ VS Code                 │",
                    "└────────┴─────────────────────────┘",
                ]
        ),
    ],
)
def test_app_sum(expected):
    result = runner.invoke(app, [])

    for line in expected:
        assert line in result.stdout
