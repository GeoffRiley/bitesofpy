from typing import List

import pytest
from regex_lookahead_lookbehind import (
    count_n_repetitions,
    count_n_reps_or_n_chars_following,
    check_surrounding_chars,
)


@pytest.mark.parametrize(
    "n, text, expected",
    [
        (1, "", 0),
        (1, "1", 0),
        (1, "11", 1),
        (2, "1", 0),
        (2, "111", 1),
        (2, "1122", 0),
        (2, "1112345", 1),
    ],
)
def test_count_n_repetitions_digits(n, text, expected):
    assert count_n_repetitions(text, n=n) == expected


@pytest.mark.parametrize(
    "n, text, expected",
    [
        (1, "a", 0),
        (1, "aa", 1),
        (1, "????{{{?}}}", 7),
        (2, "b", 0),
        (2, "ccc", 1),
        (2, "ZZaa", 0),
        (2, "ZZzz", 0),
        (2, "zzZZ", 0),
        (2, r" \\\ ", 1),
        (2, "   Spaces are fun", 1),
        (2, "\n\n\nAs are newlines\n\n\n", 2),
        (2, "As \t\t\t are tabs\t\t", 1),
    ],
)
def test_count_n_repetitions_chars(n, text, expected):
    assert count_n_repetitions(text, n=n) == expected


@pytest.mark.parametrize(
    "n, text, expected",
    [
        (1, "Ä", 0),
        (1, "ÄÄ", 1),
        (1, "※※※ - Monster Hunter - ※※※", 4),
        (2, "Ö", 0),
        (2, "ßßß", 1),
        (2, "ZZÄÄ", 0),
        (2, "Greek: εζεζεζεηηηη", 2),
    ],
)
def test_count_n_repetitions_unicode(n, text, expected):
    assert count_n_repetitions(text, n=n) == expected


@pytest.mark.parametrize(
    "n, char, text, expected",
    [
        (1, "", "", 0),
        (2, "", "1112345", 1),
        (1, "", "????{{{?}}}", 7),
        (2, "", "\n\n\nAs are newlines\n\n\n", 2),
    ],
)
def test_count_n_reps_or_n_chars_following_no_char(n, char, text, expected):
    assert count_n_reps_or_n_chars_following(text, n=n, char=char) == expected


@pytest.mark.parametrize(
    "n, char, text, expected",
    [
        (1, "z", "", 0),
        (2, "z", "1112345", 1),
        (1, "z", "????{{{?}}}", 7),
        (2, "z", "\n\n\nAs are newlines\n\n\n", 2),
    ],
)
def test_count_n_reps_or_n_chars_following_no_containing_char(n, char, text, expected):
    assert count_n_reps_or_n_chars_following(text, n=n, char=char) == expected


@pytest.mark.parametrize(
    "n, char, text, expected",
    [
        (1, "z", "zz Don't count double!", 1),
        (1, "z", "9z", 1),
        (1, "z", "9zz", 2),
        (1, "Z", "9Zz", 1),
        (1, "?", "????{{{?}}}", 8),
        (1, "[", "????[[[?]]]", 8),
        (1, "]", "????[[[?]]]", 8),
        (1, "^", "Hello^there", 2),
        (2, "z", "\n\n\nzz newlines\n\n", 2),
        (2, "a", "Kai is mean...aarg", 2),
        (2, "\t", "But bob isn't...\t\t", 2),
    ],
)
def test_count_n_reps_or_n_chars_following_mix(n, char, text, expected):
    assert count_n_reps_or_n_chars_following(text, n=n, char=char) == expected


@pytest.mark.parametrize(
    "surrounding_chars, text, expected",
    [
        (["Z", "A"], "ZZZZZ", 3),
        (["Z", "A"], "ABCCBAAAZz", 2),
        (["\n", "\t"], "\nK\nA\tI\t", 3),
        (["R", "?", "^"], "SPECIAL^C^HARS?", 2),
        (["^", "$"], "^S^tar$t$", 2),
        ([":", "|"], "?:A:lmost|t|here", 2),
    ],
)
def test_check_surrounding_chars_valid(surrounding_chars: List[str], text, expected):
    assert check_surrounding_chars(text, surrounding_chars) == expected
