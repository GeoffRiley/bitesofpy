from collections import defaultdict
from typing import List


def sum_indices(items: List[str]) -> int:
    values = defaultdict(int)
    result = 0
    for n, c in enumerate(items):
        values[c] += n
        result += values[c]
    return result
