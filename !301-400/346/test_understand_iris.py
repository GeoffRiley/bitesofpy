import numpy as np

from understand_iris import *


def test_get_nr_classes():
    assert get_nr_classes(IRIS_DATA) == 3


def test_get_nr_samples():
    assert get_nr_samples(IRIS_DATA) == 150


def test_get_nr_samples_per_class():
    np.testing.assert_allclose(get_nr_samples_per_class(IRIS_DATA), [50] * 3, rtol=1e-2)


def test_get_fraction_per_class():
    np.testing.assert_allclose(
        get_rel_nr_samples_per_class(IRIS_DATA), [0.333] * 3, rtol=1e-2
    )


def test_get_dim():
    assert get_dim(IRIS_DATA) == 4


def test_get_nr_missing_values():
    assert get_nr_missing_values(IRIS_DATA) == 0


def test_get_stats_per_feature():
    features = [
        "sepal length (cm)",
        "sepal width (cm)",
        "petal length (cm)",
        "petal width (cm)",
    ]
    stats = ["min", "max", "mean", "std"]
    expected = np.array(
        [
            [4.3, 7.9, 5.84, 0.83],
            [2, 4.4, 3.06, 0.44],
            [1, 6.9, 3.76, 1.77],
            [0.1, 2.5, 1.2, 0.76],
        ]
    ).T  # transposed because each row has all summary statistics for one feature and that is how `get_stats_per_feature` should work

    np.testing.assert_allclose(
        get_stats_per_feature(IRIS_DATA, features, stats), expected, rtol=1e-2
    )


def test_get_correlation_per_feature():
    features = [
        "sepal length (cm)",
        "sepal width (cm)",
        "petal length (cm)",
        "petal width (cm)",
    ]
    expected = np.array([0.78, -0.43, 0.95, 0.95])

    np.testing.assert_allclose(
        get_correlation_per_feature(IRIS_DATA, features), expected, rtol=1e-2
    )
