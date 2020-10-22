from typing import Dict, Any, List


def rename_keys(data: Dict[Any, Any]) -> Dict[Any, Any]:
    new_dict = dict()
    for key, val in data.items():
        if isinstance(key, str) and str(key).startswith('@'):
            key = key.lstrip('@')
        if isinstance(val, List):
            val = [rename_keys(entry) for entry in val]
        if isinstance(val, Dict):
            val = rename_keys(val)
        new_dict[key] = val
    return new_dict
