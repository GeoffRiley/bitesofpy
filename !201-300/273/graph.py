import heapq
from collections import deque


def shortest_path(graph, start, end):
    """
       Input: graph: a dictionary of dictionary
              start: starting city   Ex. a
              end:   target city     Ex. b

       Output: tuple of (distance, [path of cites])
       Ex.   (distance, ['a', 'c', 'd', 'b])
    """
    possibles = []
    history = deque([(start, end, 0, [])])
    while history:
        start_, end_, dist_, path_ = history.popleft()

        if start_ == end_:
            heapq.heappush(possibles, (dist_, path_ + [end_]))
            continue

        for nxt, dist in graph[start_].items():
            if nxt not in path_:
                history.append((nxt, end_, dist_ + dist, path_ + [start_]))

    return heapq.heappop(possibles)
