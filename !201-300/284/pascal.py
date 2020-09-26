from math import factorial
from typing import List


def pascal(N: int) -> List[int]:
    """
    Return the Nth row of Pascal triangle
    """
    row = []
    row_num = N - 1
    for n in range(N):
        row.append(int(factorial(row_num) / (factorial(n) * factorial(row_num - n))))
    return row
