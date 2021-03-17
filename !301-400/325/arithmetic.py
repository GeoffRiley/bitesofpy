import json
from typing import Generator

VALUES = "[0.1, 0.2, 0.3, 0.005, 0.005, 2.67]"


def calc_sums(values: str = VALUES) -> Generator[str, None, None]:
    """
    Process the above JSON-encoded string of values and calculate the sum of each adjacent pair.

    The output should be a generator that produces a string that recites the calculation for each pair, for example:

        'The sum of 0.1 and 0.2, rounded to two decimal places, is 0.3.'
    """
    vals = json.loads(values)
    for x, y in zip(vals[:-1], vals[1:]):
        # As we're wanting to round 0.005 up, we can add a fudge factor… URGH!
        res = round(x + y + 0.0001, 2)
        yield f'The sum of {x} and {y}, rounded to two decimal places, is {res:0.2f}.'
