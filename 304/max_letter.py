import re
from collections import Counter
from typing import Tuple

ITER_PATTERN = re.compile(r"[^\W\d_]([^\W\d_]|['-])+[^\W\d_]", flags=re.UNICODE | re.DOTALL)


def max_letter_word(text: str) -> Tuple[str, str, int]:
    """
    Find the word in text with the most repeated letters. If more than one word
    has the highest number of repeated letters choose the first one. Return a
    tuple of the word, the (first) repeated letter and the count of that letter
    in the word.
    >>> max_letter_word('I have just returned from a visit...')
    ('returned', 'r', 2)
    >>> max_letter_word('$5000 !!')
    ('', '', 0)
    """
    if not isinstance(text, str):
        raise ValueError
    word_list = dict()
    best_word = ''
    best_letter = ''
    best_repeat = 0
    for w in ITER_PATTERN.finditer(text):
        word = w.group(0)
        if word not in word_list:
            common_letter = Counter(word.casefold().replace('-', '')).most_common(1)
            word_list[word] = common_letter
            if common_letter[0][1] > best_repeat:
                best_letter, best_repeat = common_letter[0]
                best_word = word
    return best_word, best_letter, best_repeat
