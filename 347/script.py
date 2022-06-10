from enum import Enum
from typing import Optional


class Hand(str, Enum):
    RIGHT = "right"
    LEFT = "left"
    BOTH = "both"


LEFT_HAND_CHARS = set("QWERTASDFGZXCVB")
RIGHT_HAND_CHARS = set("YUIOPHJKLNM")


def get_hand_for_word(word: str) -> Hand:
    """
    Use the LEFT_HAND_CHARS and RIGHT_HAND_CHARS sets to determine
    if the passed in word can be written with only the left or right
    hand, or if both hands are needed.
    """
    result: Hand = Hand.RIGHT
    if any(c.upper() in LEFT_HAND_CHARS for c in word):
        result = Hand.LEFT
    if any(c.upper() in RIGHT_HAND_CHARS
           for c in word) and result == Hand.LEFT:
        result = Hand.BOTH

    return result
