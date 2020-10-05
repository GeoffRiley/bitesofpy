import base64
import io
import json
import os
from pathlib import Path
from typing import Dict, List

import pandas as pd  # type: ignore
import requests

URL: str = "https://bites-data.s3.us-east-2.amazonaws.com/MonthlySales.csv"
STATS: List[str] = ["sum", "mean", "max"]
TMP: Path = Path(os.getenv("TMP", "/tmp")) / "MonthlySales.csv"


def get_data(url: str) -> Dict[str, str]:
    """Get data from Github

    Args:
        url (str): The URL where the data is located.

    Returns:
        Dict[str, str]: The dictionary extracted from the data
    """
    if TMP.exists():
        data = json.loads(TMP.read_text())
    else:
        response = requests.get(url)
        response.raise_for_status()
        data = json.loads(response.text)
        with TMP.open("w") as tmp:
            json.dump(data, tmp)
    return data


def process_data(url: str) -> pd.DataFrame:
    """Process the data from the Github API

    Args:
        url (str): The URL where the data is located.

    Returns:
        pd.DataFrame: Pandas DataFrame generated from the processed data
    """
    data = get_data(url)
    # We actually want the data in the 'content', but it's base64 encoded
    useful_data = base64.b64decode(data['content'])
    # ...that needs to be turned into a stream of text...
    df = pd.read_csv(io.StringIO(useful_data.decode('utf-8')))
    # Finally we have a table of two columns 'month' and 'sales'
    # They load as strings, so they need to be turned into useful values
    df['month'] = pd.to_datetime(df['month'], format="%Y-%m-%d")
    df['sales'] = df['sales'].astype(float)
    # Fingers crossed, we can work with that!
    return df


def summary_report(df: pd.DataFrame, stats=None) -> None:
    """Summary report generated from the DataFrame and list of stats

    Will aggregate statistics for sum, mean, and max by default.

    Args:
        df (pd.DataFrame): Pandas DataFrame of the Github API data
        stats (List[str], optional): List of summaries to aggregate. Defaults to STATS.

    Returns:
        None (prints to standard output)

        Example:
                    sum          mean        max
        year
        2013  484247.51  40353.959167   81777.35
        2014  470532.51  39211.042500   75972.56
        2015  608473.83  50706.152500   97237.42
        2016  733947.03  61162.252500  118447.83
    """
    if stats is None:
        stats = STATS
    # Copy the dataframe or else it gets corrupted
    years = df.copy()
    # Give new column name for the month → year, but all columns must be listed!!
    years.columns = ['year', 'sales']
    # group the data by years and then aggregate the sales following the provided stats list
    print(years.groupby(years['year'].dt.year)['sales'].agg(stats))


def yearly_report(df: pd.DataFrame, year: int) -> None:
    """Generate a sales report for the given year

    Args:
        df (pd.DataFrame): Pandas DataFrame of the Github API data
        year (int): The year to generate the report for

    Raises:
        ValueError: Error raised if the year requested is not in the data.
        Should be in the form of "The year YEAR is not included in the report!"

    Returns:
        None (prints to standard output)

        Example:
        2013
                  sales
        month
        1      14236.90
        2       4519.89
        3      55691.01
        4      28295.35
        5      23648.29
        6      34595.13
        7      33946.39
        8      27909.47
        9      81777.35
        10     31453.39
        11     78628.72
        12     69545.62
    """
    # Extract all data that matches the given year and make a copy of it
    year_list = df[df['month'].dt.year == year].copy()
    # Check if there are records extracted
    if len(year_list) == 0:
        # if not, raise an exception
        raise ValueError(f"The year {year} is not included in the report!")
    # Set the table index to the month
    year_list = year_list.set_index(year_list['month'].dt.month)
    # Remove the actual month column so that it doesn't print
    year_list = year_list.drop(['month'], axis=1)
    print(year)
    print()  # make things line up for the tests!!
    print(year_list)
