import pytest

from script import get_spelling_suggestions, SuggestedWord


@pytest.mark.parametrize(
    "word, expected",
    [
        ("tht", [SuggestedWord(word="the", confidence=0.8636206673285276)]),
        ("drem", [SuggestedWord(word="drew", confidence=0.6348547717842323)]),
        ("responsable", [SuggestedWord(word="responsible", confidence=1.0)]),
        ("tachnical", [SuggestedWord(word="technical", confidence=1.0)]),
        ("acheive", [SuggestedWord(word="achieve", confidence=1.0)]),
        ("jkdadk", []),
        ("nigt", [SuggestedWord(word="night", confidence=0.9871794871794872)]),
    ],
)
def test_get_spelling_suggestions(word, expected):
    actual = get_spelling_suggestions(word)
    assert actual == expected


@pytest.mark.parametrize(
    "word, min_confidence, expected",
    [
        (
                "kinda",
                0.1,
                [
                    SuggestedWord(word="kind", confidence=0.8744588744588745),
                    SuggestedWord(word="kinds", confidence=0.12554112554112554),
                ],
        ),
        ("kinda", 0.2, [SuggestedWord(word="kind", confidence=0.8744588744588745)]),
        (
                "bol",
                0.1,
                [
                    SuggestedWord(word="boy", confidence=0.3797752808988764),
                    SuggestedWord(word="vol", confidence=0.18202247191011237),
                    SuggestedWord(word="box", confidence=0.16853932584269662),
                ],
        ),
        ("bol", 0.2, [SuggestedWord(word="boy", confidence=0.3797752808988764)]),
    ],
)
def test_get_spelling_suggestions_different_min_confidence(
        word, min_confidence, expected
):
    actual = get_spelling_suggestions(word, min_confidence=min_confidence)
    assert actual == expected


def test_type_of_return():
    suggestions = get_spelling_suggestions("tht")
    assert isinstance(suggestions, list)
    assert isinstance(suggestions[0], tuple)
