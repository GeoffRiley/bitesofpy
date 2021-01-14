from functools import reduce
from typing import Iterable, Set, Any


def intersection(*args: Iterable) -> Set[Any]:
    seqs = [set(a)
            for a in args
            if a is not None and len(a) > 0]
    return set() if len(seqs) == 0 else set(reduce(set.intersection, seqs))
