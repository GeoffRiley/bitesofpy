from typing import List


def make_changes(n: int, coins: List[int]) -> int:
    """
    Input: n - the changes amount
          coins - the coin denominations
    Output: how many ways to make this changes
    """
    if n == 0:
        return 1
    elif n < 0 or len(coins) == 0:
        return 0
    else:
        return make_changes(n - coins[0], coins) + make_changes(n, coins[1:])
