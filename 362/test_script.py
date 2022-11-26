import pytest
from typer.testing import CliRunner

from script import app

runner = CliRunner()

USERNAME = "Robin"
PASSWORD = "very_secure_password"


@pytest.mark.parametrize(
    "expected_result",
    [
        (
                [
                    f"Hello {USERNAME}. Doing something very secure with password.\n",
                    "...just kidding, here it is, very insecure: very_secure_password\n",
                ]
        )
    ],
)
def test_app_sum(expected_result):
    result = runner.invoke(app, [USERNAME], input=f"{PASSWORD}\n{PASSWORD}\n")

    for string_fragment in expected_result:
        assert string_fragment in result.stdout
