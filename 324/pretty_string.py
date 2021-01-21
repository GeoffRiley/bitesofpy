import pprint
from typing import Any


def pretty_string(obj: Any) -> str:
    # Format an object to a max line length of 60 chars and nestings to 2 levels
    return pprint.pformat(obj, width=60, depth=2)
