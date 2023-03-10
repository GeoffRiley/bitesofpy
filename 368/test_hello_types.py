import os
from typing import get_type_hints

import pytest
from mypy import api

from hello_types import BankAccount, greeting, headline


@pytest.fixture
def account():
    acc = BankAccount(100)
    return acc


def test_greeting_typing():
    types = get_type_hints(greeting)

    assert len(types) == 2
    assert issubclass(types["name"], str)
    assert issubclass(types["return"], str)


def test_headline_typing():
    types = get_type_hints(headline)

    assert len(types) == 4
    assert issubclass(types["text"], str)
    assert issubclass(types["centered"], bool)
    assert issubclass(types["symbol"], str)
    assert issubclass(types["return"], str)


@pytest.mark.parametrize(
    "method, expected_args, expected_return",
    [
        ("__init__", [("initial_balance", int)], type(None)),
        ("deposit", [("amount", int)], type(None)),
        ("withdraw", [("amount", int)], type(None)),
        ("overdrawn", [], bool),
    ],
)
def test_BankAccount_typing(account, method, expected_args, expected_return):
    types = get_type_hints(getattr(account, method))

    assert len(types) == len(expected_args) + 1

    for arg, arg_type in expected_args:
        assert issubclass(types[arg], arg_type)

    assert issubclass(types["return"], expected_return)


# static typed function for mypy to analyze, should find no errors in here
def mypy_good_input() -> None:
    greeting("Dear student")
    headline("Our first bite", True)
    acc = BankAccount(100)
    acc.deposit(100)
    acc.withdraw(50)


# static typed function for mypy to analyze, should find errors in here
def mypy_bad_input() -> None:
    greeting(1)
    greeting(b"Test")
    headline("Headline", "auto")
    headline("Headline", symbol=None)
    acc = BankAccount(100.5)
    acc = BankAccount()
    acc.deposit([10, 20, 30])
    acc.withdraw(0.55)


def test_mypy_report():
    tmp = "/tmp/" if "AWS_LAMBDA_FUNCTION_VERSION" in os.environ else ""
    results = api.run(
        [
            f"{tmp}test_hello_types.py",
            "--ignore-missing-imports",
            "--no-site-packages",
            "--follow-imports",
            "silent",
        ]
    )
    assert not results[1]
    assert "Found 7 errors in 1 file" in results[0]
