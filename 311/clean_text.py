import re
import string
import sys
from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile

import pandas as pd

TMP = Path("/tmp")
S3 = "https://bites-data.s3.us-east-2.amazonaws.com"


def _setup():
    data_zipfile = '311-data.zip'
    urlretrieve(f'{S3}/{data_zipfile}', TMP / data_zipfile)
    ZipFile(TMP / data_zipfile).extractall(TMP)
    sys.path.append(TMP)


_setup()

from stop_words import stop_words
from tf_idf import TFIDF


def load_data() -> pd.DataFrame:
    # Load the text and populate a Pandas Dataframe
    # The order of the sample text strings should not be changed
    # Return the Dataframe with the index and 'text' column
    filename = TMP / "samples.txt"
    df = pd.read_csv(filename)
    return df


def strip_url_email(x_df: pd.DataFrame) -> pd.DataFrame:
    # Strip all URLs (http://...) and Emails (somename@email.address)
    # The 'text' column should be modified to remove
    #   all URls and Emails
    regex_pat = re.compile(r'(?:https?:\S+|(:?\S\.?)+@(?:\S\.?)+)', re.IGNORECASE)
    x_df['text'] = x_df['text'].str.replace(regex_pat, '')
    return x_df


def to_lowercase(x_df: pd.DataFrame) -> pd.DataFrame:
    # Convert the contents of the 'text' column to lower case
    # Return the Dataframe with the 'text' as lower case
    x_df['text'] = x_df['text'].str.lower()
    return x_df


def stripline_stopwords(line: str) -> str:
    result = []
    for word in line.split():
        if word not in stop_words:
            result.append(word)
    return ' '.join(result)


def strip_stopwords(x_df: pd.DataFrame) -> pd.DataFrame:
    # Drop all stop words from the 'text' column
    # Return the Dataframe with the 'text' stripped of stop words
    x_df['text'] = x_df['text'].apply(stripline_stopwords)
    return x_df


def stripline_non_ascii(line: str) -> str:
    result = ''
    for c in line:
        if c.isascii():
            result += c
    return result


def strip_non_ascii(x_df: pd.DataFrame) -> pd.DataFrame:
    # Remove all non-ascii characters from the 'text' column
    # Return the Dataframe with the 'text' column
    #   stripped of non-ascii characters
    x_df['text'] = x_df['text'].apply(stripline_non_ascii)
    return x_df


def strip_digits_punctuation(x_df: pd.DataFrame) -> pd.DataFrame:
    # Remove all digits and punctuation characters from the 'text' column
    # Return the Dataframe with the 'text' column
    #   stripped of all digit and punctuation characters
    regex_pat = re.compile(fr'(?:\d+|[{string.punctuation}]+)', re.IGNORECASE)
    x_df['text'] = x_df['text'].str.replace(regex_pat, '')
    return x_df


def calculate_tfidf(x_df: pd.DataFrame) -> pd.DataFrame:
    # Calculate the 'tf-idf' matrix of the 'text' column
    # Return the 'tf-idf' Dataframe
    tfidf_obj = TFIDF(x_df["text"])
    return tfidf_obj()


def sort_columns(x_df: pd.DataFrame) -> pd.DataFrame:
    # Depending on how the earlier functions are implemented
    #   it's possible that the order of the columns may be different
    # Sort the 'tf-idf' Dataframe columns
    #   This ensure the tests are compatible
    x_df = x_df.sort_index(axis=1)
    return x_df


def get_tdidf() -> pd.DataFrame:
    # Pandas’ pipeline feature allows you to string together
    #   Python functions in order to build a pipeline of data processing.
    # Complete the functions above in order to produce a 'tf-idf' Dataframe
    # Return the 'tf-idf' Dataframe
    df = (
        load_data()
            .pipe(strip_url_email)
            .pipe(to_lowercase)
            .pipe(strip_stopwords)
            .pipe(strip_non_ascii)
            .pipe(strip_digits_punctuation)
            .pipe(calculate_tfidf)
            .pipe(sort_columns)
    )
    return df
