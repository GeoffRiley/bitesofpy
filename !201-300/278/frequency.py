from collections import Counter


def major_n_minor(numbers):
    """
    Input: an array with integer numbers
    Output: the majority and minority number
    """
    c = Counter(numbers)
    commons = c.most_common()
    major = commons[0][0]
    minor = commons[-1][0]

    return major, minor
