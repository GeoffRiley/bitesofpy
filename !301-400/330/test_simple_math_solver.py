import pytest

from simple_math_solver import find_all_solutions


@pytest.mark.parametrize(
    "operations,numerical_result,correct_solution",
    [
        # simple equations
        (  # simple addition
                ["+"],
                6,
                [
                    [1, 5],
                    [2, 4],
                    [4, 2],
                    [5, 1],
                ],
        ),
        (  # simple subtraction
                ["-"],
                6,
                [
                    [7, 1],
                    [8, 2],
                    [9, 3],
                ],
        ),
        (  # simple multiplication
                ["*"],
                6,
                [
                    [1, 6],
                    [2, 3],
                    [3, 2],
                    [6, 1],
                ],
        ),
        # two operators
        (  # multiplication then subtraction
                ["*", "-"],
                16,
                [[3, 6, 2], [3, 7, 5], [4, 6, 8], [6, 3, 2], [6, 4, 8], [7, 3, 5]],
        ),
        (  # subtraction then multiplication
                ["-", "*"],
                -16,
                [[2, 3, 6], [2, 6, 3], [5, 3, 7], [5, 7, 3], [8, 4, 6], [8, 6, 4]],
        ),
        # more complex equations and answers
        (  # complex equation
                ["+", "*", "*", "+", "*", "-"],
                528,
                [
                    [6, 7, 8, 9, 4, 5, 2],
                    [6, 7, 8, 9, 5, 4, 2],
                    [6, 7, 9, 8, 4, 5, 2],
                    [6, 7, 9, 8, 5, 4, 2],
                    [6, 8, 7, 9, 4, 5, 2],
                    [6, 8, 7, 9, 5, 4, 2],
                    [6, 8, 9, 7, 4, 5, 2],
                    [6, 8, 9, 7, 5, 4, 2],
                    [6, 9, 7, 8, 4, 5, 2],
                    [6, 9, 7, 8, 5, 4, 2],
                    [6, 9, 8, 7, 4, 5, 2],
                    [6, 9, 8, 7, 5, 4, 2],
                ],
        ),
        (  # long multiplication with many solutions
                ["*", "*", "*", "*"],
                5040,
                [
                    [2, 5, 7, 8, 9],
                    [2, 5, 7, 9, 8],
                    [2, 5, 8, 7, 9],
                    [2, 5, 8, 9, 7],
                    [2, 5, 9, 7, 8],
                    [2, 5, 9, 8, 7],
                    [2, 7, 5, 8, 9],
                    [2, 7, 5, 9, 8],
                    [2, 7, 8, 5, 9],
                    [2, 7, 8, 9, 5],
                    [2, 7, 9, 5, 8],
                    [2, 7, 9, 8, 5],
                    [2, 8, 5, 7, 9],
                    [2, 8, 5, 9, 7],
                    [2, 8, 7, 5, 9],
                    [2, 8, 7, 9, 5],
                    [2, 8, 9, 5, 7],
                    [2, 8, 9, 7, 5],
                    [2, 9, 5, 7, 8],
                    [2, 9, 5, 8, 7],
                    [2, 9, 7, 5, 8],
                    [2, 9, 7, 8, 5],
                    [2, 9, 8, 5, 7],
                    [2, 9, 8, 7, 5],
                    [3, 5, 6, 7, 8],
                    [3, 5, 6, 8, 7],
                    [3, 5, 7, 6, 8],
                    [3, 5, 7, 8, 6],
                    [3, 5, 8, 6, 7],
                    [3, 5, 8, 7, 6],
                    [3, 6, 5, 7, 8],
                    [3, 6, 5, 8, 7],
                    [3, 6, 7, 5, 8],
                    [3, 6, 7, 8, 5],
                    [3, 6, 8, 5, 7],
                    [3, 6, 8, 7, 5],
                    [3, 7, 5, 6, 8],
                    [3, 7, 5, 8, 6],
                    [3, 7, 6, 5, 8],
                    [3, 7, 6, 8, 5],
                    [3, 7, 8, 5, 6],
                    [3, 7, 8, 6, 5],
                    [3, 8, 5, 6, 7],
                    [3, 8, 5, 7, 6],
                    [3, 8, 6, 5, 7],
                    [3, 8, 6, 7, 5],
                    [3, 8, 7, 5, 6],
                    [3, 8, 7, 6, 5],
                    [5, 2, 7, 8, 9],
                    [5, 2, 7, 9, 8],
                    [5, 2, 8, 7, 9],
                    [5, 2, 8, 9, 7],
                    [5, 2, 9, 7, 8],
                    [5, 2, 9, 8, 7],
                    [5, 3, 6, 7, 8],
                    [5, 3, 6, 8, 7],
                    [5, 3, 7, 6, 8],
                    [5, 3, 7, 8, 6],
                    [5, 3, 8, 6, 7],
                    [5, 3, 8, 7, 6],
                    [5, 6, 3, 7, 8],
                    [5, 6, 3, 8, 7],
                    [5, 6, 7, 3, 8],
                    [5, 6, 7, 8, 3],
                    [5, 6, 8, 3, 7],
                    [5, 6, 8, 7, 3],
                    [5, 7, 2, 8, 9],
                    [5, 7, 2, 9, 8],
                    [5, 7, 3, 6, 8],
                    [5, 7, 3, 8, 6],
                    [5, 7, 6, 3, 8],
                    [5, 7, 6, 8, 3],
                    [5, 7, 8, 2, 9],
                    [5, 7, 8, 3, 6],
                    [5, 7, 8, 6, 3],
                    [5, 7, 8, 9, 2],
                    [5, 7, 9, 2, 8],
                    [5, 7, 9, 8, 2],
                    [5, 8, 2, 7, 9],
                    [5, 8, 2, 9, 7],
                    [5, 8, 3, 6, 7],
                    [5, 8, 3, 7, 6],
                    [5, 8, 6, 3, 7],
                    [5, 8, 6, 7, 3],
                    [5, 8, 7, 2, 9],
                    [5, 8, 7, 3, 6],
                    [5, 8, 7, 6, 3],
                    [5, 8, 7, 9, 2],
                    [5, 8, 9, 2, 7],
                    [5, 8, 9, 7, 2],
                    [5, 9, 2, 7, 8],
                    [5, 9, 2, 8, 7],
                    [5, 9, 7, 2, 8],
                    [5, 9, 7, 8, 2],
                    [5, 9, 8, 2, 7],
                    [5, 9, 8, 7, 2],
                    [6, 3, 5, 7, 8],
                    [6, 3, 5, 8, 7],
                    [6, 3, 7, 5, 8],
                    [6, 3, 7, 8, 5],
                    [6, 3, 8, 5, 7],
                    [6, 3, 8, 7, 5],
                    [6, 5, 3, 7, 8],
                    [6, 5, 3, 8, 7],
                    [6, 5, 7, 3, 8],
                    [6, 5, 7, 8, 3],
                    [6, 5, 8, 3, 7],
                    [6, 5, 8, 7, 3],
                    [6, 7, 3, 5, 8],
                    [6, 7, 3, 8, 5],
                    [6, 7, 5, 3, 8],
                    [6, 7, 5, 8, 3],
                    [6, 7, 8, 3, 5],
                    [6, 7, 8, 5, 3],
                    [6, 8, 3, 5, 7],
                    [6, 8, 3, 7, 5],
                    [6, 8, 5, 3, 7],
                    [6, 8, 5, 7, 3],
                    [6, 8, 7, 3, 5],
                    [6, 8, 7, 5, 3],
                    [7, 2, 5, 8, 9],
                    [7, 2, 5, 9, 8],
                    [7, 2, 8, 5, 9],
                    [7, 2, 8, 9, 5],
                    [7, 2, 9, 5, 8],
                    [7, 2, 9, 8, 5],
                    [7, 3, 5, 6, 8],
                    [7, 3, 5, 8, 6],
                    [7, 3, 6, 5, 8],
                    [7, 3, 6, 8, 5],
                    [7, 3, 8, 5, 6],
                    [7, 3, 8, 6, 5],
                    [7, 5, 2, 8, 9],
                    [7, 5, 2, 9, 8],
                    [7, 5, 3, 6, 8],
                    [7, 5, 3, 8, 6],
                    [7, 5, 6, 3, 8],
                    [7, 5, 6, 8, 3],
                    [7, 5, 8, 2, 9],
                    [7, 5, 8, 3, 6],
                    [7, 5, 8, 6, 3],
                    [7, 5, 8, 9, 2],
                    [7, 5, 9, 2, 8],
                    [7, 5, 9, 8, 2],
                    [7, 6, 3, 5, 8],
                    [7, 6, 3, 8, 5],
                    [7, 6, 5, 3, 8],
                    [7, 6, 5, 8, 3],
                    [7, 6, 8, 3, 5],
                    [7, 6, 8, 5, 3],
                    [7, 8, 2, 5, 9],
                    [7, 8, 2, 9, 5],
                    [7, 8, 3, 5, 6],
                    [7, 8, 3, 6, 5],
                    [7, 8, 5, 2, 9],
                    [7, 8, 5, 3, 6],
                    [7, 8, 5, 6, 3],
                    [7, 8, 5, 9, 2],
                    [7, 8, 6, 3, 5],
                    [7, 8, 6, 5, 3],
                    [7, 8, 9, 2, 5],
                    [7, 8, 9, 5, 2],
                    [7, 9, 2, 5, 8],
                    [7, 9, 2, 8, 5],
                    [7, 9, 5, 2, 8],
                    [7, 9, 5, 8, 2],
                    [7, 9, 8, 2, 5],
                    [7, 9, 8, 5, 2],
                    [8, 2, 5, 7, 9],
                    [8, 2, 5, 9, 7],
                    [8, 2, 7, 5, 9],
                    [8, 2, 7, 9, 5],
                    [8, 2, 9, 5, 7],
                    [8, 2, 9, 7, 5],
                    [8, 3, 5, 6, 7],
                    [8, 3, 5, 7, 6],
                    [8, 3, 6, 5, 7],
                    [8, 3, 6, 7, 5],
                    [8, 3, 7, 5, 6],
                    [8, 3, 7, 6, 5],
                    [8, 5, 2, 7, 9],
                    [8, 5, 2, 9, 7],
                    [8, 5, 3, 6, 7],
                    [8, 5, 3, 7, 6],
                    [8, 5, 6, 3, 7],
                    [8, 5, 6, 7, 3],
                    [8, 5, 7, 2, 9],
                    [8, 5, 7, 3, 6],
                    [8, 5, 7, 6, 3],
                    [8, 5, 7, 9, 2],
                    [8, 5, 9, 2, 7],
                    [8, 5, 9, 7, 2],
                    [8, 6, 3, 5, 7],
                    [8, 6, 3, 7, 5],
                    [8, 6, 5, 3, 7],
                    [8, 6, 5, 7, 3],
                    [8, 6, 7, 3, 5],
                    [8, 6, 7, 5, 3],
                    [8, 7, 2, 5, 9],
                    [8, 7, 2, 9, 5],
                    [8, 7, 3, 5, 6],
                    [8, 7, 3, 6, 5],
                    [8, 7, 5, 2, 9],
                    [8, 7, 5, 3, 6],
                    [8, 7, 5, 6, 3],
                    [8, 7, 5, 9, 2],
                    [8, 7, 6, 3, 5],
                    [8, 7, 6, 5, 3],
                    [8, 7, 9, 2, 5],
                    [8, 7, 9, 5, 2],
                    [8, 9, 2, 5, 7],
                    [8, 9, 2, 7, 5],
                    [8, 9, 5, 2, 7],
                    [8, 9, 5, 7, 2],
                    [8, 9, 7, 2, 5],
                    [8, 9, 7, 5, 2],
                    [9, 2, 5, 7, 8],
                    [9, 2, 5, 8, 7],
                    [9, 2, 7, 5, 8],
                    [9, 2, 7, 8, 5],
                    [9, 2, 8, 5, 7],
                    [9, 2, 8, 7, 5],
                    [9, 5, 2, 7, 8],
                    [9, 5, 2, 8, 7],
                    [9, 5, 7, 2, 8],
                    [9, 5, 7, 8, 2],
                    [9, 5, 8, 2, 7],
                    [9, 5, 8, 7, 2],
                    [9, 7, 2, 5, 8],
                    [9, 7, 2, 8, 5],
                    [9, 7, 5, 2, 8],
                    [9, 7, 5, 8, 2],
                    [9, 7, 8, 2, 5],
                    [9, 7, 8, 5, 2],
                    [9, 8, 2, 5, 7],
                    [9, 8, 2, 7, 5],
                    [9, 8, 5, 2, 7],
                    [9, 8, 5, 7, 2],
                    [9, 8, 7, 2, 5],
                    [9, 8, 7, 5, 2],
                ],
        ),
    ],
    ids=[
        "simple addition",
        "simple subtraction",
        "simple multiplication",
        "multiplication then subtraction",
        "subtraction then multiplication",
        "complex equation",
        "long multiplication with many solutions",
    ],
)
def test_results(operations, numerical_result, correct_solution):
    returned_solutions = list(find_all_solutions(operations, numerical_result))
    assert sorted(returned_solutions) == sorted(correct_solution)


@pytest.mark.parametrize(
    "operations,result",
    [
        (["x"], 0),  # Operator not supported
        (["+", "-", "*", "/"], 55),  # Operator not supported"
        (["+"], 55.2),  # float result
    ],
    ids=[
        "non-supported operator x",
        "non-supported operator /",
        "result of type float",
    ],
)
def test_incorrect_input(operations, result):
    with pytest.raises(ValueError):
        list(find_all_solutions(operations, result))