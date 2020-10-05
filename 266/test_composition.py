from abc import ABCMeta
from dataclasses import dataclass
from urllib.error import URLError

import pytest  # type: ignore
from composition import (
    TMP,
    TODAY,
    File,
    LeaderBoard,
    NYTimes,
    Poll,
    RealClearPolitics,
    Site,
    Soup,
    Web,
)

CLEAN_UP = False


@pytest.fixture(scope="module")
def test_file():
    file = File("test.html")
    yield file
    if CLEAN_UP:
        if file.path.exists():
            file.path.unlink()


@pytest.fixture(scope="module")
def rcp():
    rcp_file = File("realclearpolitics.html")
    rcp_url = (
        "https://bites-data.s3.us-east-2.amazonaws.com/"
        "2020-03-10_realclearpolitics.html"
    )
    rcp_web = Web(rcp_url, rcp_file)
    yield RealClearPolitics(rcp_web)
    if CLEAN_UP:
        if rcp_web.file.path.exists():
            rcp_web.file.path.unlink()


@pytest.fixture(scope="module")
def nyt():
    nyt_file = File("nytimes.html")
    nyt_url = ("https://bites-data.s3.us-east-2.amazonaws.com/"
               "2020-03-10_nytimes.html")
    nyt_web = Web(nyt_url, nyt_file)
    yield NYTimes(nyt_web)
    if CLEAN_UP:
        if nyt_web.file.path.exists():
            nyt_web.file.path.unlink()


def test_file_class():
    file = File("empty.html")
    # Fix to accept DOS pathnames on a Windoze machine
    assert str(file.path) == f"{TMP}/{TODAY}_{file.name}" or str(file.path) == f"{TMP}\\{TODAY}_{file.name}"
    assert file.data is None


def test_web(test_file):
    url = "https://projects.fivethirtyeight.com/polls/"
    test_web = Web(url, test_file)
    assert test_web.url == url
    assert isinstance(test_web.file, File)
    assert isinstance(test_web.soup, Soup)


def test_web_bad_url():
    file = File("clamytoe.html")
    url = "https://clamytoe.dev"
    test_web = Web(url, file)
    with pytest.raises(URLError) as e:
        test_web.data
    error = str(e.value)
    assert 'urlopen error' in error
    assert ('Name or service not known' in error
            or 'nodename nor servname provided, or not known' in error)


def test_poll(rcp):
    table = rcp.find_table()
    rows = rcp.parse_rows(table)
    poll = rows[0]
    assert isinstance(rows, list)
    assert isinstance(poll, Poll)
    assert isinstance(poll.Sanders, float)


def test_leaderboard(nyt):
    table = nyt.find_table()
    rows = nyt.parse_rows(table)
    leaderboard = rows[0]
    assert isinstance(rows, list)
    assert isinstance(leaderboard, LeaderBoard)
    assert isinstance(leaderboard.Delegates, int)
    assert isinstance(leaderboard.Coverage, int)


def test_rcp_stats(rcp, capfd):
    expected = {"Biden": 1244.0, "Sanders": 1248.0, "Gabbard": 64.0}
    rcp.stats(3)
    output = capfd.readouterr()[0].splitlines()
    assert "RealClearPolitics" in output
    assert f"{'=' * 17}" in output
    candidates = {}
    for candidate in output[3:-1]:
        name, votes = candidate.strip().split(": ")
        candidates[name] = float(votes)
    assert candidates["Biden"] == expected["Biden"]
    assert candidates["Sanders"] == expected["Sanders"]
    assert candidates["Gabbard"] == expected["Gabbard"]


def test_nyt(nyt, capfd):
    nyt.stats()
    output = capfd.readouterr()[0].splitlines()
    assert f"{'=' * 33}" in output
    assert f"{'-' * 33}" in output
    assert "National Polling Average: 29%" in output
    assert "       Pledged Delegates: 610" in output
    assert "Individual Contributions: $11.1m" in output
    assert "    Weekly News Coverage: 3" in output


def test_site(test_file):
    Site.__abstractmethods__ = set()

    @dataclass
    class Dummy(Site):
        web: Web

    url = "https://projects.fivethirtyeight.com/polls/"
    test_web = Web(url, test_file)
    d = Dummy(test_web)
    table = d.find_table()
    rows = d.parse_rows(table)
    polls = d.polls()
    stats = d.stats()
    assert d.web.file.name == "test.html"
    assert isinstance(Site, ABCMeta)
    assert rows is None
    assert polls is None
    assert stats is None
