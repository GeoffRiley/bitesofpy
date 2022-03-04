import math

import numpy as np
import pytest

from metropolis_hastings import metropolis_hastings

np.random.seed(42)


def norm_dist(x, mean, std):
    """Gaussian normal probability distribution."""
    return np.exp(-0.5 * (x - mean) ** 2 / std ** 2)


def standard_norm_dist(x):
    """Gaussian normal standard probability distribution."""
    return norm_dist(x, mean=0, std=1)


def custom_norm_dist(x):
    """Gaussian normal probability distribution with mean of 1 and standard deviation of two."""
    return norm_dist(x, mean=1, std=2)


def exp_dist(x, lambda_):
    """Exponential probability distribution."""
    return lambda_ * np.exp(-lambda_ * x) if x >= 0 else 0


def custom_exp_dist(x):
    return exp_dist(x, lambda_=10)


def test_correctness():
    samples = metropolis_hastings(standard_norm_dist, 0, 100)
    assert len(samples) == 100
    assert isinstance(samples, np.ndarray)
    assert np.issubdtype(samples.dtype, np.floating)


def test_raise_exception_for_non_functions():
    with pytest.raises(TypeError):
        samples = metropolis_hastings(sum([]))
        

@pytest.mark.parametrize("n_samples", [-1, -10, -100, 0,])
def test_raise_exception_for_wrong_n_samples(n_samples):
    with pytest.raises(ValueError):
        samples = metropolis_hastings(standard_norm_dist, 0, n_samples)


@pytest.mark.parametrize(
    "f, x_0, expected_mean, expected_std",
    [
        (standard_norm_dist, 0, 0, 1),
        (standard_norm_dist, 1, 0, 1),
        (standard_norm_dist, -1, 0, 1),
        (custom_norm_dist, 0, 1, 2),
        (custom_norm_dist, 1, 1, 2),
        (custom_norm_dist, -1, 1, 2),
        (custom_exp_dist, 0, 1 / 10, math.sqrt(1 / 10 ** 2)),
    ],
)
def test_univariate_functions(f, x_0, expected_mean, expected_std):
    samples = metropolis_hastings(f, x_0)
    np.testing.assert_almost_equal(samples.mean(), expected_mean, decimal=1)
    np.testing.assert_almost_equal(samples.std(), expected_std, decimal=1)