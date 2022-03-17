from typing import Callable

import numpy as np


def metropolis_hastings(f: Callable,
                        x_0: float = 0.0,
                        n_samples: int = 10000) -> np.ndarray:
    """Implements the metropolis-hastings algorithm with a normal distribution as proposal function.

    Args:
        f (Callable): An arbitrary probability density function
            that is used to calculate the acceptance ratio alpha=f(x_next)/f(x_t).
            f has to accept a single parameter x and return the function value for x.
        x_0 (float, optional): The first observation to start from.
        n_samples (int, optional): Number of samples to be drawn. Defaults to 10000.

    Returns:
        (np.ndarray): Drawn samples from the target distribution.
    """
    # Sanity check: have to be looking for a positive quantity of result
    # values.
    if n_samples <= 0:
        raise ValueError('Cannot request less than one sample')

    # Two different 'random' functions:
    #  the first returns values from a normal distribution, using the loc
    #   parameter to ensure that the random values are centered around the
    #   previous value; and
    #  the second returns values from a uniform distribution of values
    #   between 0.0 and 1.0.
    norm_rnd = np.random.normal
    uni_rnd = np.random.uniform

    # Build a list of results starting with the first value given.
    result = [x_0]
    # Always keep a track of the previous value and it's computed value.
    x_t, f_x_t = x_0, f(x_0)
    # Build the array until it holds n_samples.
    # for _ in range(n_samples - 1):
    while len(result) < n_samples:
        # Pick a new value centered around the previous value, and compute
        # it's functional value.
        x_next = norm_rnd(loc=x_t)
        f_x_next = f(x_next)
        # Compare the computed ratio with a uniform random value to deside
        # if the selected value is acceptable.
        if uni_rnd() > (f_x_next / f_x_t):
            # If not, then repeat the previous value
            x_next, f_x_next = x_t, f_x_t
        # Add the selected value to the results and remember as the previous
        # values.
        result.append(x_next)
        x_t, f_x_t = x_next, f_x_next

    return np.array(result)
