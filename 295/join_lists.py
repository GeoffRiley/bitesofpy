from typing import List, Union


def join_lists(lst_of_lst: List[List[str]], sep: str) -> Union[List[str], None]:
    if len(lst_of_lst) == 0:
        return None
    res = []
    while len(lst_of_lst) > 0:
        res.extend([sep, *lst_of_lst.pop(0)])
    return res[1:]
