from typing import Dict


def decompress(string: str, table: Dict[str, str]) -> str:
    res = ''
    for ch in string:
        if ch in table:
            res += decompress(table[ch], table)
        else:
            res += ch
    return res
