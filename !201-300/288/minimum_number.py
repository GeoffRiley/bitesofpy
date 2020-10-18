from typing import List


def minimum_number(digits: List[int]) -> int:
    if len(digits) == 0:
        digits = [0]
    return int(''.join(str(d) for d in sorted(set(digits))))
