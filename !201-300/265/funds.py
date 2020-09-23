IMPOSSIBLE = 'Mission impossible. No one can contribute.'


def max_fund(village):
    """Find a contiguous subarray with the largest sum."""
    best = (0, 0, 0)
    for end in range(len(village)):
        for start in range(0, end):
            running = sum(village[start:end + 1])  # remember that the end of a slice is exclusive
            if running > best[0]:
                best = (running, start + 1, end + 1)
    if best[0] == 0:
        print(IMPOSSIBLE)
    return best
