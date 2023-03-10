def original_expected_value(n: int) -> float:
    """Calculate the expected value of an n-sided die."""
    multiplicand = 1 / n
    series = [multiplicand * (i + 1) for i in range(n)]
    return round(sum(series), 3)


def new_expected_value(n: int) -> float:
    """Calculate the expected value of an n-sided die when the player simulaneously rolls
    two dice and chooses the larger value.
    """
    dividend = n ** 2
    series = [(1 + 2 * i) / dividend * (i + 1) for i in range(n)]
    return round(sum(series), 3)
