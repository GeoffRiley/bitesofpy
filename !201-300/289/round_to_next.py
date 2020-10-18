import math


def sgn(x: int) -> int:
    return 1 if x > 0 else -1 if x < 0 else 0
    # return int(math.copysign(1, x))  # slower


def round_to_next(number: int, multiple: int):
    return math.floor((number + multiple - sgn(multiple)) / multiple) * multiple
