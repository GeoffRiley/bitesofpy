import pytest

from strings import common_words

sentence1 = ['To', 'be', 'or', 'not', 'to', 'be',
             'that', 'is', 'a', 'question']
sentence2 = ['To', 'strive', 'to', 'seek', 'to',
             'find', 'and', 'not', 'to', 'yield']
sentence3 = ['No', 'two', 'persons', 'ever', 'to',
             'read', 'the', 'same', 'book', 'You', 'said']
sentence4 = ['The', 'more', 'read', 'the',
             'more', 'things', 'will', 'know']
sentence5 = ['be', 'a', 'good', 'man']


@pytest.mark.parametrize("sentence1, sentence2, expected", [
    (sentence1, sentence2, ['to', 'not']),
    (sentence3, sentence4, ['the', 'read']),
    (sentence2, sentence3, ['to']),
    (sentence5, sentence1, ['a', 'be']),
])
def test_common_words(sentence1, sentence2, expected):
    actual = common_words(sentence1, sentence2)
    assert actual == expected
