import os
from collections.abc import Iterable, Iterator
from typing import Union, get_args, get_origin, get_type_hints

from mypy import api

from advanced_types import (
    fib,
    greet_all,
    greeting,
    normalize_id,
    nums_below,
    stars,
)


def test_stars_typing():
    types = get_type_hints(stars)

    assert len(types) == 3, "Expected 2 typed arguments and one typed return value"
    assert issubclass(types["args"], int), "args should be compatible with type int"
    assert issubclass(
        types["kwargs"], float
    ), "kwargs should be compatible with type float"
    assert issubclass(types["return"], type(None)), "return type should be NoneType"


def test_fib_typing():
    types = get_type_hints(fib)

    assert len(types) == 2, "Expected 1 typed argument and one typed return value"
    assert issubclass(types["n"], int), "n should be compatible with type int"
    assert issubclass(
        get_origin(types["return"]), Iterator
    ), "return type should be compatible with Iterator"
    assert (
            len(get_args(types["return"])) == 1
    ), "Iterator return type should have one type subscription"
    assert issubclass(
        get_args(types["return"])[0], int
    ), "Iterator return type should have one type subscription compatible with int"


def test_greet_all_typing():
    types = get_type_hints(greet_all)

    assert len(types) == 2, "Expected 1 typed argument and one typed return value"
    assert issubclass(
        get_origin(types["names"]), Iterable
    ), "names should be compatible with Iterable"
    assert (
            len(get_args(types["names"])) == 1
    ), "names Iterator should have one type subscription"
    assert issubclass(
        get_args(types["names"])[0], str
    ), "names Iterator should have one type subscription compatible with str"
    assert issubclass(
        types["return"], type(None)
    ), "return type should be compatible with NoneType"


def test_greeting_typing():
    types = get_type_hints(greeting)

    assert len(types) == 2, "Expected 1 typed argument and one typed return value"
    assert get_origin(types["name"]) is Union, "name should be compatible with Union"
    assert (
            len(get_args(types["name"])) == 2
    ), "name should be compatible with Union having 2 type subscriptions"
    assert issubclass(
        get_args(types["name"])[0], str
    ), "name should be compatible with Union having 2 type subscriptions, one being str"
    assert issubclass(types["return"], str), "return type should be compatible with str"


def test_normalize_id_typing():
    types = get_type_hints(normalize_id)

    assert len(types) == 2, "Expected 1 typed argument and one typed return value"
    assert (
            get_origin(types["user_id"]) is Union
    ), "user_id should be compatible with Union"
    assert (
            len(get_args(types["user_id"])) == 2
    ), "user_id should be compatible with Union having 2 type subscriptions"
    assert set(get_args(types["user_id"])) == set(
        (int, str)
    ), "user_id should be compatible with Union having 2 type subscriptions, either int or str"
    assert issubclass(types["return"], str), "return type should be compatible with str"


def test_nums_below_typing():
    types = get_type_hints(nums_below)

    assert len(types) == 3
    assert issubclass(get_origin(types["numbers"]), Iterable)
    assert len(get_args(types["numbers"])) == 1
    assert issubclass(get_args(types["numbers"])[0], float)
    assert issubclass(types["limit"], float)
    assert get_origin(types["return"]) is list
    assert issubclass(get_args(types["return"])[0], float)


# static typed function for mypy to analyze, should find no errors in here
def mypy_good_input() -> None:
    stars(1, 2, 3, key1=1.0, key2=2.0)
    stars(1, 2, 3, key1=1, key2=2)
    fib_iter = fib(5)
    next(fib_iter)
    greet_all(["Michael", "Bob", "Erik"])
    greet_all(("Michael", "Bob", "Erik"))
    greet_all({"Michael", "Bob", "Erik"})
    greet_all("Michael Bob Erik")
    greet_all({"name1": "Michael", "name2": "Bob"})
    greeting()
    greeting("Michael")
    greeting(None)
    normalize_id(42)
    normalize_id("42")
    nums_below([1.1, 2.2, 3.3], 0.5)
    nums_below((1, 2, 3), -1)
    nums_below({1.1, 2.2, 3.3}, 55.83)
    nums = nums_below([1.1, 2.2, 3.3], 3)
    nums.append(0.5)
    nums.append(1)


# static typed function for mypy to analyze, should find errors in here
def mypy_bad_input() -> None:
    stars(1.0, 2j, "3", key1=1.0, key2=2.0)
    stars(1, 2, 3, key1="1.0", key2=2.0)
    stars(1, 2, 3, key1=1.0, key2=2j)
    _ = fib(5.0)
    _ = fib("5")
    greet_all([1, 2.0, True])
    greet_all({1: "Michael", (2,): "Bob"})
    greeting(42)
    greeting(["Michael", "Erik"])
    normalize_id(42.0)
    normalize_id(None)
    nums_below(["1.0", 1j, (1,)], 0.5)
    nums_below({1.1, 2.2, 3.3}, "1")
    nums = nums_below([1.1, 2.2, 3.3], 3.1)
    nums.append(1j)


def test_mypy_report():
    tmp = "/tmp/" if "AWS_LAMBDA_FUNCTION_VERSION" in os.environ else ""
    results = api.run(
        [
            f"{tmp}test_advanced_types.py",
            "--ignore-missing-imports",
            "--no-site-packages",
            "--follow-imports",
            "silent",
        ]
    )

    print(results[0])
    assert not results[1]
    assert "Found 21 errors in 1 file" in results[0]
