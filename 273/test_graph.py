from graph import shortest_path

simple = {
    'a': {'b': 2, 'c': 4, 'e': 1},
    'b': {'a': 2, 'd': 3},
    'c': {'a': 4, 'd': 6},
    'd': {'c': 6, 'b': 3, 'e': 2},
    'e': {'a': 1, 'd': 2}
}

major = {
    'a': {'w': 14, 'x': 7, 'y': 9},
    'b': {'w': 9, 'z': 6},
    'w': {'a': 14, 'b': 9, 'y': 2},
    'x': {'a': 7, 'y': 10, 'z': 15},
    'y': {'a': 9, 'w': 2, 'x': 10, 'z': 11},
    'z': {'b': 6, 'x': 15, 'y': 11},
}


def test_graph_simple():
    actual = shortest_path(simple, 'a', 'd')
    expected = (3, ['a', 'e', 'd'])
    assert actual == expected


def test_graph_major():
    actual = shortest_path(major, 'a', 'b')
    expected = (20, ['a', 'y', 'w', 'b'])
    assert actual == expected
