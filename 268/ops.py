from collections import deque


def num_ops(n):
    """
    Input: an integer number, the target number
    Output: the minimum number of operations required to reach to n from 1.

    Two operations rules:
    1.  multiply by 2
    2.  int. divide by 3

    The base number is 1. Meaning the operation will always start with 1
    These rules can be run in any order, and can be run independently.

    [Hint] the data structure is the key to solve it efficiently.
    """
    target = n
    # Here lies a fudge to stop large numbers running away for too long
    # surely there's a better way?
    ten_target = target * 10
    track = 1
    ops_num = 0
    # keep a running history of where we've been and where we're going next
    visited = []
    history = deque([(track, ops_num)])

    while history:

        track, ops_num = history.popleft()
        if track == target:
            break

        ops_num += 1
        if (track * 2) not in visited and track < ten_target:
            new_track = track * 2
            visited.append(new_track)
            history.append((new_track, ops_num))

        if (track // 3) not in visited:
            new_track = track // 3
            visited.append(new_track)
            history.append((new_track, ops_num))

    return ops_num
