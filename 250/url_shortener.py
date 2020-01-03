from string import ascii_lowercase, ascii_uppercase, digits
from typing import Dict

CODEX: str = digits + ascii_lowercase + ascii_uppercase
BASE: int = len(CODEX)
# makeshift database record
LINKS: Dict[int, str] = {
    1: "https://pybit.es",
    45: "https://pybit.es/pages/articles.html",
    255: "http://pbreadinglist.herokuapp.com",
    600: "https://pybit.es/pages/challenges.html",
    874: "https://stackoverflow.com",
}
SITE: str = "https://pybit.es"

# error messages
INVALID = "Not a valid PyBites shortened url"
NO_RECORD = "Not a valid shortened url"


def encode(record: int) -> str:
    """Encodes an integer into Base62"""
    res = ''
    while record > 0:
        res = CODEX[record % BASE] + res
        record = record // BASE
    return res


def decode(short_url: str) -> int:
    """Decodes the Base62 string into a Base10 integer"""
    res = 0
    c = 0
    while len(short_url) > c:
        res = res * BASE + CODEX.index(short_url[c])
        c += 1
    return res


def redirect(url: str) -> str:
    """Retrieves URL from shortened DB (LINKS)

    1. Check for valid domain
    2. Check if record exists
    3. Return URL stored in LINKS or proper message
    """
    if not url.startswith(SITE):
        return INVALID
    ind = decode(url[len(SITE) + 1:])
    if not ind in LINKS:
        return NO_RECORD
    return LINKS[ind]


def shorten_url(url: str, next_record: int) -> str:
    """Shortens URL and updates the LINKS DB

    1. Encode next_record
    2. Adds url to LINKS
    3. Return shortened URL
    """
    ind = encode(next_record)  # could be max(LINKS.keys())
    LINKS[next_record] = url
    return f'{SITE}/{ind}'
