import re
from typing import List, Sequence


def extract_ipv4(data):
    """
    Given a nested list of data return a list of IPv4 address information that can be extracted
    """
    return walk_list(data)


def walk_list(data) -> List[tuple]:
    result = []
    if len(data) == 0:
        return result
    m = {}
    data_it = iter(data)
    element = next(data_it)
    try:
        while True:
            if isinstance(element, str):
                if str(element).lower() in ['ip', 'mask', 'type']:
                    m[element] = next(data_it)[0]
                    if len(m) == 3:
                        if (
                                str(m['type']) == 'ip_mask' and
                                str(m['mask']).isdecimal() and
                                re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}',
                                         str(m['ip']).strip('"'))
                        ):
                            result.append((m['ip'].strip('"'), m['mask']))
                            m.clear()
            elif isinstance(element, Sequence):
                result.extend(walk_list(element))
            element = next(data_it)
    except StopIteration:
        pass
    return result
