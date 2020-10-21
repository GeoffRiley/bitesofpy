from itertools import zip_longest
from typing import List


def jagged_list(lst_of_lst: List[List[int]], fillvalue: int = 0) -> List[List[int]]:
    return [list(lst)
            for lst in zip(*[lst
                             for lst in zip_longest(*lst_of_lst, fillvalue=fillvalue)
                             ])
            ]
