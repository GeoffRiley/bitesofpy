import builtins
import importlib.util
import keyword
from typing import Dict, List

scores = {
    "builtin": 1,
    "keyword": 2,
    "module": 3,
}


def score_objects(objects: List[str],
                  scores: Dict[str, int] = scores) -> int:
    result = 0
    for o in objects:
        if o in dir(builtins):
            result += scores['builtin']
        if keyword.iskeyword(o):
            result += scores['keyword']
        try:
            if importlib.util.find_spec(o) is not None:
                result += scores['module']
        except AttributeError:
            pass
        except ModuleNotFoundError:
            pass
    return result
