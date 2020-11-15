import math


def calc_median_from_dict(d: dict) -> float:
    """
    :param d: dict of numbers and their occurrences
    :return: float: median
    Example:
    {1: 2, 3: 1, 4: 2} -> [1, 1, 3, 4, 4] --> 3 is median
    """
    # Work out where in the list the median will lie
    median_loc = sum(d.values()) / 2
    median_base = math.ceil(median_loc)
    # If could be between two values!
    split = float(median_base) == median_loc

    # Keep a running total
    cumulative = 0
    # Get a list of the keys nicely sorted for reference
    sorted_keys = list(sorted(d.keys()))

    # Work through the keys, the enumeration lets us work out what the
    # next value is too
    for n, key1 in enumerate(sorted_keys):
        # Work out the next key --- be aware it might be at the end
        key2 = sorted_keys[min(n + 1, len(sorted_keys) - 1)]

        # Update the running total
        cumulative = cumulative + d[key1]

        # ... and see if we're in the right place
        if cumulative == median_base:
            # On the boundary, check if the median is between the two values
            if split:
                return (key1 + key2) / 2
            else:
                return key1
        elif cumulative > median_base:
            # Overshot, the median was in that block
            return key1
