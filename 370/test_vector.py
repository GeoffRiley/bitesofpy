import os
from typing import List, Union, get_origin, get_type_hints

import pytest
from mypy import api

from vector import Vector


@pytest.mark.parametrize(
    "method, nr_types, return_type",
    [
        ("__init__", 4, type(None)),
        ("from_list", 2, Vector),
        ("norm", 2, float),
        ("iscollinear", 2, bool),
        ("angle", 2, float),
        ("__getitem__", 2, float),
        ("__call__", 1, tuple),
        ("__len__", 1, int),
        ("__add__", 2, Vector),
        ("__sub__", 2, Vector),
        ("__mul__", 2, Union),
        ("__rmul__", 2, Union),
        ("__str__", 1, str),
        ("__repr__", 1, str),
    ],
)
def test_correct_number_of_type_hints(method, nr_types, return_type):
    v = Vector(1, 1, 1)
    types = get_type_hints(getattr(v, method))
    print(types)
    assert len(types) == nr_types
    try:
        assert issubclass(types["return"], return_type)
    except TypeError:
        assert get_origin(types["return"]) is return_type


# static typed function for mypy to analyze, should find no errors in here
def mypy_good_input() -> None:
    Vector(1, 1, 1)
    Vector(True, False, True)
    Vector(1.0, 2.5, 0.7)
    Vector(-1, -2, -0.123)
    Vector.from_list([1, 2, 3])
    Vector.from_list([1.1, 0.7, -0.23])
    Vector.from_list([1, 2, 3, 4])  # oops
    isinstance(Vector.from_list([1, 2, 3]), Vector)
    Vector.from_list([1, 2, 3])
    Vector(0.5, 0.5, 0.5).norm(1)
    Vector(1, 1, 1).iscollinear(Vector(2, 2, 2))
    Vector(1, 1, 1).angle(Vector(1, 2, 3))
    Vector(1, 1, 1)[1]
    x, y, z = Vector(1, 1, 1)()
    Vector(1, 1, 1) + Vector(1, 1, 1)
    Vector(1, 1, 1) - Vector(1, 1, 1)
    Vector(1, 1, 1) * 0, 5
    0.5 * Vector(1, 1, 1)
    Vector(1, 1, 1) * Vector(2, 2, 2)


# static typed function for mypy to analyze, should find errors in here
def mypy_bad_input() -> None:
    Vector("1", 1, 1)
    Vector(1, "1", 1)
    Vector(1, 1, "1")
    Vector([1], (2,), {3})  # actually three errors
    Vector.from_list((1, 2, 3))
    Vector.from_list({1, 2, 3})
    Vector.from_list("123")
    v: List[float] = Vector.from_list([1, 2, 3])
    Vector(0.5, 0.5, 0.5).norm("2")
    Vector(0.5, 0.5, 0.5).norm(2.5)
    Vector(1, 1, 1).iscollinear(True)
    Vector(1, 1, 1).iscollinear("Vector(1,2,3)")
    Vector(1, 1, 1).iscollinear([2, 2, 2])
    Vector(1, 1, 1).angle(False)
    Vector(1, 1, 1).angle("Vector(1,2,3)")
    Vector(1, 1, 1).angle([1, 2, 3])
    Vector(1, 1, 1)[1.1]
    Vector(1, 1, 1)["1"]
    Vector(1, 1, 1)[[1, 2]]
    Vector(1, 1, 1)[1:2]
    x, y, z, _ = Vector(1, 1, 1)()
    x, y = Vector(1, 1, 1)()
    Vector(1, 1, 1) + 1
    Vector(1, 1, 1) + "Vector(1,1,1)"
    Vector(1, 1, 1) + [1, 1, 1]
    Vector(1, 1, 1) - 0.7
    Vector(1, 1, 1) - "Vector(1,1,1)"
    Vector(1, 1, 1) - [1, 1, 1]
    Vector(1, 1, 1) * "Vector(1,1,1)"
    "Vector(1,1,1)" * Vector(1, 1, 1)
    Vector(1, 1, 1) * [1, 1, 1]
    [1, 1, 1] * Vector(1, 1, 1)
    Vector(1, 1, 1) * {1, 1, 1}
    {1, 1, 1} * Vector(1, 1, 1)


def test_mypy_report():
    tmp = "/tmp/" if "AWS_LAMBDA_FUNCTION_VERSION" in os.environ else ""
    results = api.run(
        [
            f"{tmp}test_vector.py",
            "--ignore-missing-imports",
            "--no-site-packages",
            "--follow-imports",
            "silent",
        ]
    )

    print(results[0])
    assert not results[1]
    assert "Found 36 errors in 1 file" in results[0]
