import re


def count_n_repetitions(text, n=1):
    """
    Counts how often characters are followed by themselves for
    n times.

    text: UTF-8 compliant input text
    n: How often character should be repeated, defaults to 1
    """
    match = re.findall(
        rf'((.)(?=\2{{{n}}}))',
        text,
        re.DOTALL + re.UNICODE)

    return len(match)


def count_n_reps_or_n_chars_following(text, n=1, char=""):
    """
    Counts how often characters are repeated for n times, or
    followed by char n times.

    text: UTF-8 compliant input text
    n: How often character should be repeated, defaults to 1
    char: Character which also counts if repeated n times
    """
    if not char:
        return count_n_repetitions(text, n)

    match = re.findall(
        rf'((.)(?=((\2){{{n}}}|{re.escape(char)}{{{n}}})))',
        text,
        re.DOTALL | re.UNICODE)

    return len(match)


def check_surrounding_chars(text, surrounding_chars):
    """
    Count the number of times a character is surrounded by
    characters from the surrounding_chars list.

    text: UTF-8 compliant input text
    surrounding_chars: List of characters
    """
    s = ''.join(re.escape(char) for char in surrounding_chars)
    match = re.findall(
        rf'((?<=[{s}])(.)(?=[{s}]))',
        text,
        re.DOTALL | re.UNICODE)

    return len(match)
