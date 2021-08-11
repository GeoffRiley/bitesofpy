from itertools import permutations
from operator import add, sub, mul
from typing import List, Union, Iterable, Any

ALLOWED_OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul
}


def compute(values: List[Any], ops_list: List[Any]) -> int:
    vals = values.copy()
    ops = ops_list.copy()
    result = vals.pop(0)
    while ops:
        o = ops.pop(0)
        nxt = vals.pop(0)
        # if there's a multiplication coming up, do that first
        while ops and ops[0] == mul:
            ops.pop(0)
            nxt *= vals.pop(0)
        result = o(result, nxt)
    return result


def find_all_solutions(
        operator_path: List[str], expected_result: int
) -> Union[List[List[int]], Iterable[List[int]]]:
    result = []
    # Verify parameters
    if not isinstance(expected_result, int):
        raise ValueError('None integer result value provided')
    ops = []
    for i in operator_path:
        if i not in ALLOWED_OPERATORS:
            raise ValueError('Only + - and * are allowed operators')
        ops.append(ALLOWED_OPERATORS[i])
    if len(ops) > 10:
        raise ValueError('Too many operators')

    for val_set in permutations(range(1, 10), len(operator_path) + 1):
        val_set = list(val_set)
        if compute(val_set, ops) == expected_result:
            result.append(val_set)
    return result
