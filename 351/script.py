from typing import List, NamedTuple

from textblob import Word

MIN_CONFIDENCE = 0.5


# define SuggestedWord NamedTuple with attributes
# word (str) and confidence (float)
class SuggestedWord(NamedTuple):
    word: str
    confidence: float


def get_spelling_suggestions(
        word: str, min_confidence: float = MIN_CONFIDENCE
) -> List[SuggestedWord]:
    """
    Find spelling suggestions with at least minimum confidence score
    Use textblob.Word (check out the docs)
    """
    result = []
    for suggest in Word(word).spellcheck():
        suggested_word = SuggestedWord(*suggest)
        if suggested_word.confidence >= min_confidence:
            result.append(suggested_word)

    return result
