import enum
from dataclasses import dataclass
from typing import List


class BiteLevel(enum.IntEnum):
    INTRO = 1
    BEGINNER = 2
    INTERMEDIATE = 3
    ADVANCED = 4


@dataclass
class Bite:
    number: int
    title: str
    level: BiteLevel

    def __gt__(self, other):
        return self.number > other.number


def create_bites(numbers: List[int], titles: List[str],
                 levels: List[BiteLevel]):
    """Generate a generator of Bite dataclass objects"""
    for n, t, l in zip(numbers, titles, levels):
        yield Bite(n, t, l)
