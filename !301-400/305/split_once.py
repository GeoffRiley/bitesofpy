from typing import List


def split_once(text: str, separators: str = None) -> List[str]:
    if separators is None:
        separators = ' \t\n\r\v\f'
    separators = set(separators)
    res = []
    pos = 0
    start_pos = pos
    while pos < len(text) and len(separators) > 0:
        while pos < len(text) and text[pos] not in separators:
            pos += 1
        if pos < len(text):
            separators.remove(text[pos])
        res.append(text[start_pos:pos])
        pos += 1
        start_pos = pos
    if len(res) == 0 or start_pos < len(text):
        res.append(text[start_pos:])
    return res
