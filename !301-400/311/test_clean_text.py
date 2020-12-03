import pandas as pd
import pytest
from clean_text import (strip_url_email,
                        to_lowercase,
                        strip_stopwords,
                        strip_non_ascii,
                        strip_digits_punctuation,
                        get_tdidf,
                        TMP)
from pandas._testing import assert_frame_equal

df_samples = pd.read_pickle(TMP / "samples.pkl")


def get_df_column(column_name):
    return df_samples[[column_name]].rename(columns={column_name: "text"})


# Call get_tfidf() and get the coded solution
df_act = get_tdidf()

# Read the expected solution from file
df_exp = pd.read_csv(TMP / "tf-idf.csv")


# Compare the solution to the expected solution
@pytest.mark.parametrize(
    "test_input, expected",
    [
        (get_df_column("text"), get_df_column("strip_url_email")),
        (
                pd.DataFrame(
                    [
                        "this is a url http://www.pybites.com in the middle of other text",
                        "this is an email bob@pybites.com in the middle of other text",
                        "no url or email",
                    ],
                    columns=["text"],
                ),
                pd.DataFrame(
                    [
                        "this is a url  in the middle of other text",
                        "this is an email  in the middle of other text",
                        "no url or email",
                    ],
                    columns=["text"],
                ),
        ),
    ],
)
def test_strip_url_email(test_input, expected):
    returned_values = strip_url_email(test_input)
    assert_frame_equal(returned_values, expected)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (get_df_column("strip_url_email"), get_df_column("to_lowercase")),
        (
                pd.DataFrame(
                    [
                        "this is the first test string, it has no upper case letters",
                        "THIS IS THE SECOND TEST STRING, IT IS ALL UPPER CASE",
                        "This is the Third Sting. It is MIXED CASE",
                    ],
                    columns=["text"],
                ),
                pd.DataFrame(
                    [
                        "this is the first test string, it has no upper case letters",
                        "this is the second test string, it is all upper case",
                        "this is the third sting. it is mixed case",
                    ],
                    columns=["text"],
                ),
        ),
    ],
)
def test_to_lowercase(test_input, expected):
    returned_values = to_lowercase(test_input)
    assert_frame_equal(returned_values, expected)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (get_df_column("to_lowercase"), get_df_column("strip_stopwords")),
        (
                pd.DataFrame(
                    [
                        "i me my myself we our ours ourselves you",
                        "i me my myself we our ours ourselves you hello world",
                        "lorem ipsum dolor sit amet, consectetur adipiscing elit",
                    ],
                    columns=["text"],
                ),
                pd.DataFrame(
                    [
                        "",
                        "hello world",
                        "lorem ipsum dolor sit amet, consectetur adipiscing elit",
                    ],
                    columns=["text"],
                ),
        ),
    ],
)
def test_strip_stopwords(test_input, expected):
    returned_values = strip_stopwords(test_input)
    assert_frame_equal(returned_values, expected)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (get_df_column("strip_stopwords"), get_df_column("strip_non_ascii")),
        (
                pd.DataFrame(
                    [
                        "this test has no non ascii characters",
                        "lots of non ascii characters 🐵🙈🙉🙊❤️💔💌💕💞",
                    ],
                    columns=["text"],
                ),
                pd.DataFrame(
                    [
                        "this test has no non ascii characters",
                        "lots of non ascii characters ",
                    ],
                    columns=["text"],
                ),
        ),
    ],
)
def test_strip_non_ascii(test_input, expected):
    returned_values = strip_non_ascii(test_input)
    assert_frame_equal(returned_values, expected)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (get_df_column("strip_non_ascii"), get_df_column("strip_digits_punctuation")),
        (
                pd.DataFrame(
                    [
                        "this test has no special characters",
                        "lots of punctuation characters ,$%^&*<>?|&*():+_'",
                        "lots of digits 1234567891012121314",
                    ],
                    columns=["text"],
                ),
                pd.DataFrame(
                    [
                        "this test has no special characters",
                        "lots of punctuation characters ",
                        "lots of digits ",
                    ],
                    columns=["text"],
                ),
        ),
    ],
)
def test_strip_digits_punctuation(test_input, expected):
    returned_values = strip_digits_punctuation(test_input)
    assert_frame_equal(returned_values, expected)


# Compare the solution to the expected solution
@pytest.mark.parametrize("test_input, expected", [(df_act, df_exp)])
def test_tfidf(test_input, expected):
    assert_frame_equal(test_input, expected)
