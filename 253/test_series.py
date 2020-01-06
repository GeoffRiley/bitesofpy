import string

import pandas as pd
import pytest
import series as se

file_name = "https://bites-data.s3.us-east-2.amazonaws.com/iris.csv"
df = pd.read_csv(file_name)


@pytest.fixture()
def sepal_length_series():
    """Returns the Sepal Length Series from the Iris DataFrame"""
    return df.sepal_length.sort_values().reset_index(drop=True)


@pytest.fixture()
def int_series_vsmall():
    """Returns a pandas Series containing ints"""
    return pd.Series(range(1, 6))


@pytest.fixture()
def int_series_small():
    """Returns a pandas Series containing ints"""
    return pd.Series(range(10))


@pytest.fixture()
def int_series_vsmall_offset_index():
    """Returns a pandas Series containing ints"""
    return pd.Series(range(0, 10, 2), index=range(0, 10, 2))


@pytest.fixture()
def letters_series():
    """Returns a pandas Series containing all lower case letters"""
    return pd.Series(list(string.ascii_lowercase))


@pytest.mark.parametrize(
    "arg, expected",
    [
        (("add", 5), [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]),
        (("add", 0), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
        (("add", -15), [-15, -14, -13, -12, -11, -10, -9, -8, -7, -6]),
        (("sub", 5), [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4]),
        (("sub", 0), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
        (("sub", -15), [15, 16, 17, 18, 19, 20, 21, 22, 23, 24]),
        (("mul", 5), [0, 5, 10, 15, 20, 25, 30, 35, 40, 45]),
        (("mul", 0), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        (("mul", -15), [0, -15, -30, -45, -60, -75, -90, -105, -120, -135]),
        (("div", 5), [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8]),
        (("div", -5), [-0.0, -0.2, -0.4, -0.6, -0.8, -1.0,
                       -1.2, -1.4, -1.6, -1.8]),
    ],
)
def test_series_simple_math(int_series_small, arg, expected):
    assert all(
        expected[idx] == val
        for idx, val in enumerate(
            se.series_simple_math(int_series_small, arg[0], arg[1])
        )
    )


@pytest.mark.parametrize(
    "arg, expected",
    [
        ("add", [1.0, "nan", 5.0, "nan", 9.0, "nan", "nan"]),
        ("sub", [1.0, "nan", 1.0, "nan", 1.0, "nan", "nan"]),
        ("mul", [0.0, "nan", 6.0, "nan", 20.0, "nan", "nan"]),
        ("div", ["inf", "nan", 1.5, "nan", 1.25, "nan", "nan"]),
    ],
)
def test_complex_series_maths(
        int_series_vsmall, int_series_vsmall_offset_index, arg, expected
):
    result = se.complex_series_maths(
        int_series_vsmall, int_series_vsmall_offset_index, arg
    )
    result = ",".join(str(n) for n in result)
    expected = ",".join(str(n) for n in expected)
    assert result == expected


@pytest.mark.parametrize(
    "arg, expected",
    [
        (
                ["a", "e", "i", "o", "u"],
                [
                    True,
                    False,
                    False,
                    False,
                    True,
                    False,
                    False,
                    False,
                    True,
                    False,
                    False,
                    False,
                    False,
                    False,
                    True,
                    False,
                    False,
                    False,
                    False,
                    False,
                    True,
                    False,
                    False,
                    False,
                    False,
                    False,
                ],
        ),
        (
                ["j", "k", "q", "x", "z"],
                [
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    True,
                    True,
                    False,
                    False,
                    False,
                    False,
                    False,
                    True,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    True,
                    False,
                    True,
                ],
        ),
    ],
)
def test_create_series_mask(letters_series, arg, expected):
    result = se.create_series_mask(letters_series, arg)
    assert all([result[idx] == exp for idx, exp in enumerate(expected)])
    assert all(l in arg for l in letters_series[result])


def test_custom_series_function(sepal_length_series):
    result = se.custom_series_function(sepal_length_series, 0.1)
    assert len(result) == 51
    assert round(result.mean(), 4) == 5.6725
    assert max(result.index) == 149 and max(result.values) == 7.9
    assert min(result.index) == 0 and min(result.values) == 4.3
    assert result[82] == 5.9
    assert result.iloc[10] == 5.0
    assert result.iloc[11] == 5.1
    assert result.iloc[20] == 5.7
    assert result.iloc[37] == 5.9
    assert result.iloc[38] == 6.4
