from itertools import chain
from typing import Sequence

TYPE_ERROR_MSG = "Unsupported input type: use either a list or a tuple"
VALUE_ERROR_MSG = "Unsupported input value: citations cannot be neither empty nor None"


def _verify_citations(citations):
    if citations is None:
        raise ValueError(VALUE_ERROR_MSG)
    if not isinstance(citations, (list, tuple)):
        raise TypeError(TYPE_ERROR_MSG)
    if not citations or any(not isinstance(x, int) or x < 0 for x in set(citations)):
        raise ValueError(VALUE_ERROR_MSG)


def h_index(citations: Sequence[int]) -> int:
    """Return the highest number of papers h having at least h citations"""
    _verify_citations(citations)
    sorted_citations = sorted(citations, reverse=True)

    return max(chain([0], (n for n, x in enumerate(sorted_citations, start=1) if x >= n)))


def i10_index(citations: Sequence[int]) -> int:
    """Return the number of papers having at least 10 citations"""
    _verify_citations(citations)

    return sum(1 for n in citations if n >= 10)
