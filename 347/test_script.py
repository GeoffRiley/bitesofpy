import pytest

from script import Hand, get_hand_for_word


@pytest.mark.parametrize("word, expected", [
    ("aam", Hand.BOTH),
    ("unpicketed", Hand.BOTH),
    ("muscot", Hand.BOTH),
    ("aspirer", Hand.BOTH),
    ("quadribasic", Hand.BOTH),
    ("holothurioid", Hand.BOTH),
    ("cloamen", Hand.BOTH),
    ("antereformational", Hand.BOTH),
    ("baal", Hand.BOTH),
    ("moirette", Hand.BOTH),
    ("terret", Hand.LEFT),
    ("refederate", Hand.LEFT),
    ("awee", Hand.LEFT),
    ("crewer", Hand.LEFT),
    ("addressee", Hand.LEFT),
    ("reaward", Hand.LEFT),
    ("verve", Hand.LEFT),
    ("tearcat", Hand.LEFT),
    ("extra", Hand.LEFT),
    ("Geez", Hand.LEFT),
    ("exeat", Hand.LEFT),
    ("Hui", Hand.RIGHT),
    ("miny", Hand.RIGHT),
    ("kinkly", Hand.RIGHT),
    ("Lui", Hand.RIGHT),
    ("pull", Hand.RIGHT),
    ("kop", Hand.RIGHT),
    ("Ji", Hand.RIGHT),
    ("nymph", Hand.RIGHT),
    ("unjoin", Hand.RIGHT),
    ("Luo", Hand.RIGHT),
])
def test_get_hand_for_word(word, expected):
    result = get_hand_for_word(word)
    assert result == expected