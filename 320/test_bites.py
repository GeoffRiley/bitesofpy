import dataclasses
import enum
import operator

import pytest

from bites import BiteLevel, create_bites

NUMBERS = [101, 1, 97, 2]
TITLES = 'f-string,sum numbers,scrape holidays,regex fun'.split(',')


@pytest.fixture(scope="module")
def some_bites():
    return list(create_bites(NUMBERS, TITLES,
                             BiteLevel.__members__.values()))


def test_bite_level_type():
    assert type(BiteLevel) is enum.EnumMeta


@pytest.mark.parametrize(
    "level, score",
    zip(BiteLevel.__members__.keys(), range(1, 5))
)
def test_bite_level_values(level, score):
    assert getattr(BiteLevel, level) == score


def test_create_bites_return_objects(some_bites):
    assert all(dataclasses.is_dataclass(bite) for bite in some_bites)


def test_create_bites_content(some_bites):
    assert [b.number for b in some_bites] == NUMBERS
    assert [b.title for b in some_bites] == TITLES
    assert [b.level for b in some_bites] == list(BiteLevel.__members__.values())


def test_create_bites_can_be_sorted(some_bites):
    first, *_, last = sorted(some_bites)
    assert first.number == 1
    assert last.number == 101
    first, *_, last = sorted(some_bites, key=operator.attrgetter('level'),
                             reverse=True)
    assert first.level == BiteLevel.ADVANCED
    assert last.level == BiteLevel.INTRO
