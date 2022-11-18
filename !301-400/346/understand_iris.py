__all__ = [
    "IRIS_DATA",
    "get_nr_classes",
    "get_nr_samples",
    "get_dim",
    "get_nr_samples_per_class",
    "get_rel_nr_samples_per_class",
    "get_nr_missing_values",
    "get_stats_per_feature",
    "get_correlation_per_feature",
]  # __all__ controls what gets imported if you use `from module.py import *`.

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.utils import Bunch

# you can set as_frame to False, but this will complicate the solution
# because you have to work with numpy ndarrays
IRIS_DATA: Bunch = load_iris(as_frame=True, return_X_y=True)


def get_nr_classes(data: Bunch) -> int:
    """Return the number of classes in the Iris data set.

    Arguments:
        data (tuple): The data as returned by sklearn.datasets.load_iris().

    Returns:
        int: Number of classes (targets) in the data set.
    """
    return len(set(data[1]))


def get_nr_samples(data: Bunch) -> int:
    """Return the number of samples in the Iris data set.

    Arguments:
        data (tuple): The data as returned by sklearn.datasets.load_iris().

    Returns:
        int: Number of samples (instances) in the data set.
    """
    return data[0].shape[0]


def get_dim(data: Bunch) -> int:
    """Return the dimensionality of the Iris data set.

    **Warning**: Dimensionality is not meant in the mathematical sense
        (which would be the shape and dim attribute if we would talk about
        matrices). Dimensionality in ML means the number of dimensions in your
        data, that is the number of axes your data span over, which is the
        number of features we have available.

    Arguments:
        data (tuple): The data as returned by sklearn.datasets.load_iris().

    Returns:
        int: Number of dimensions (features) in the data set.
    """
    return data[0].shape[1]


def get_nr_samples_per_class(data: Bunch) -> pd.Series:
    """Return the number of samples for each class of the Iris data set.

    Arguments:
        data (tuple): The data as returned by sklearn.datasets.load_iris().

    Returns:
        pd.Series: Series with number of samples for each class.
    """
    return data[1].value_counts()


def get_rel_nr_samples_per_class(data: Bunch) -> pd.Series:
    """Return the relative number of samples for each class of the Iris data
        set.

    **Hint**: Try to re-use already defined functions.
    
    Arguments:
        data (tuple): The data as returned by sklearn.datasets.load_iris().

    Returns:
        pd.Series: Series with percentage (between 0 and 1) of samples for
            each class.
    """
    return get_nr_samples_per_class(data) / get_nr_samples(data)


def get_nr_missing_values(data: Bunch) -> int:
    """Return the number of missing values in the Iris data set.
    
    **Hint**: pandas `isna()` might come in handy.

    Arguments:
        data (tuple): The data as returned by sklearn.datasets.load_iris().

    Returns:
        int: Number of missing values in the data set.
    """
    # sum can only sum along axis 0 (indices) or 1 (columns), so we need to
    # call it twice
    na_array = data[0].isna()
    count_axis1 = na_array.sum(1)
    count_axis0 = count_axis1.sum(0)
    return int(count_axis0)


def get_stats_per_feature(
        data: Bunch,
        features: list,
        stats: list,
) -> pd.DataFrame:
    """Return summary statistics for a list of given features.
    
    **Hint**: Maybe try out pandas.DataFrame.describe() or 
        pandas.DataFrame.agg().

    Arguments:
        data (tuple): The data as returned by sklearn.datasets.load_iris().
        features (list): A list of features for which to calculate summary
            statistics.
        stats (list): A list of summary statistics to calculate/extract for
            the given features.

    Returns:
        pd.DataFrame: A data frame with the requested summary statistics for
            each feature.
    """
    selected_features = data[0][features]
    return selected_features.describe().loc[stats]


def get_correlation_per_feature(
        data: Bunch,
        features: list,
) -> pd.DataFrame:
    """Return feature correlation with target.
    
    **Hint**: Correlation coefficients can be calculated for each pair of
        feature with pandas.DataFrame.corr(). This means you might have
        to combine the features and the target into a single data frame.

    Arguments:
        data (tuple): The data as returned by sklearn.datasets.load_iris().
        features (list): A list with feature names for which the correlation
            is returned.

    Returns:
        pd.Series: Value of feature correlation with target.
    """
    joined_dataframes = data[0].join(data[1])
    correlation = joined_dataframes.corr()[data[1].name]

    return correlation.loc[features]


if __name__ == "__main__":
    # here you can try out your functions!
    # only called when directly run so no problem when imported from the test
    # file
    print(IRIS_DATA[0].head())  # show the first 5 lines.
    print(get_nr_classes(
        IRIS_DATA))  # pass the data to the function and return nr classes.
