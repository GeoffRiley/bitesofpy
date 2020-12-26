import logging
from typing import List  # python 3.9 we can drop this

logger = logging.getLogger('app')


def sum_even_numbers(numbers: List[float]) -> float:
    """
    1. Of the numbers passed in sum the even ones
       and return the result.
    2. If all goes well log an INFO message:
       Input: {numbers} -> output: {ret}
    3. If bad inputs are passed in
       (e.g. one of the numbers is a str), catch
       the exception log it, then reraise it.
    """
    try:
        result = sum(n for n in numbers if not (n % 2))
        logger.info(f'Input: {numbers} -> output: {result}')
    except TypeError as e:
        logger.error(f'Bad inputs: {numbers}', exc_info=True)
        raise e
    return result
