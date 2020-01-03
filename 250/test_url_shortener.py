import pytest

from url_shortener import decode, encode, redirect, shorten_url


@pytest.mark.parametrize(
    "arg, expected",
    [
        (1, "1"),
        (45, "J"),
        (255, "47"),
        (600, "9G"),
        (874, "e6"),
        (1024, "gw"),
        (2048, "x2"),
        (3072, "Ny"),
        (4096, "144"),
        (5120, "1kA"),
    ],
)
def test_encode(arg, expected):
    assert encode(arg) == expected


@pytest.mark.parametrize(
    "arg, expected",
    [
        ("3W", 244),
        ("1bO", 4576),
        ("5e", 324),
        ("co", 768),
        ("18h", 4357),
        ("1Yk", 7584),
        ("3M", 234),
        ("jnRFH", 286438245),
    ],
)
def test_decode(arg, expected):
    assert decode(arg) == expected


@pytest.mark.parametrize(
    "url, next_record, expected",
    [
        ("https://google.com", 5000, "https://pybit.es/1iE"),
        ("https://youtube.com", 6000, "https://pybit.es/1yM"),
        ("https://python.org", 7000, "https://pybit.es/1OU"),
        ("https://medium.com", 8000, "https://pybit.es/252"),
        ("https://tryexceptpass.org", 9000, "https://pybit.es/2la"),
        ("https://training.talkpython.fm", 9999, "https://pybit.es/2Bh"),
    ],
)
def test_shorten_url(url, next_record, expected):
    assert shorten_url(url, next_record) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://pybit.es/1", "https://pybit.es"),
        ("https://pybit.es/J", "https://pybit.es/pages/articles.html"),
        ("https://pybit.es/47", "http://pbreadinglist.herokuapp.com"),
        ("https://pybit.es/9G", "https://pybit.es/pages/challenges.html"),
        ("https://pybit.es/e6", "https://stackoverflow.com"),
    ],
)
def test_redirect(url, expected):
    assert redirect(url) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://pybit.es/1iE", "https://google.com"),
        ("https://pybit.es/1yM", "https://youtube.com"),
        ("https://pybit.es/1OU", "https://python.org"),
        ("https://pybit.es/252", "https://medium.com"),
        ("https://pybit.es/2la", "https://tryexceptpass.org"),
        ("https://pybit.es/2Bh", "https://training.talkpython.fm"),
        ("https://pybit.es/bites", "Not a valid shortened url"),
        ("https://youtu.be/gAYL5H46QnQ", "Not a valid PyBites shortened url"),
    ]
)
def test_modified_links(url, expected):
    assert redirect(url) == expected
