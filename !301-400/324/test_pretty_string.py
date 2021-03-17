import pytest

from pretty_string import pretty_string


@pytest.mark.parametrize(
    "input_obj, expected_result",
    [
        (list(range(10)), "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"),
        (
                [["A"] * 11, ["A"] * 12],
                (
                        "[['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A'],\n"
                        " ['A',\n"
                        "  'A',\n"
                        "  'A',\n"
                        "  'A',\n"
                        "  'A',\n"
                        "  'A',\n"
                        "  'A',\n"
                        "  'A',\n"
                        "  'A',\n"
                        "  'A',\n"
                        "  'A',\n"
                        "  'A']]"
                ),
        ),
        ([1, [2, [3, [4]]]], "[1, [2, [...]]]"),
        (
                ["a" * 30] + [["b" * 30]] + [[3.0, [1]]],
                "['aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',\n"
                " ['bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'],\n"
                " [3.0, [...]]]",
        ),
        ({"z": 1, "c": 2, "a": 3}, "{'a': 3, 'c': 2, 'z': 1}"),
        (
                {
                    "font-family": "serif",
                    "speak": "none",
                    "font-style": "normal",
                    "font-weight": "400",
                    "font-variant": "normal",
                    "text-transform": "none",
                    "line-height": "1",
                },
                (
                        "{'font-family': 'serif',\n"
                        " 'font-style': 'normal',\n"
                        " 'font-variant': 'normal',\n"
                        " 'font-weight': '400',\n"
                        " 'line-height': '1',\n"
                        " 'speak': 'none',\n"
                        " 'text-transform': 'none'}"
                ),
        ),
    ],
)
def test_pretty_str(input_obj, expected_result):
    result = pretty_string(input_obj)
    assert result == expected_result
