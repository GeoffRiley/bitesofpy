import re
from numbers import Number
from typing import Union

# use lookbehind and lookforward to find the places where changes occur
symbol_split = re.compile(r'((?<!^)(?=[A-Z])|(?<!\d)(?=[0-9]))')


# digit_split = re.compile(r'(?<!\d)(?=\d)')


def to_snake_case(a_string: str) -> str:
    result = symbol_split.sub('_', a_string).lower()
    return result.replace('-', '_')


def snake_case_keys(data: Union[dict, str, Number]):
    # Strings and numbers pass back unaltered
    if isinstance(data, (str, Number)):
        return data
    # Dictionaries look through to migrate the key names
    if isinstance(data, dict):
        return {to_snake_case(k): snake_case_keys(v) for k, v in data.items()}
    # Lists just process the list to cater for embedded dictionaries
    if isinstance(data, list):
        return [snake_case_keys(v) for v in data]
    raise TypeError(f'Unknown type encountered: {data.__class__}')
