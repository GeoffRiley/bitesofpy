from typing import List, TypeVar

T = TypeVar('T', int, float)


def n_digit_numbers(numbers: List[T], n: int) -> List[int]:
    extras = '0' * n
    ret = [int(f'{v}{extras}'.replace('.', '')[:n + (1 if v < 0 else 0)]) for v in numbers]
    return ret
