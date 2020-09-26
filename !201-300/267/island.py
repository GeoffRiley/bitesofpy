# Hint:
# You can define a helper function: get_others(map, row, col) to assist you.
# Then in the main island_size function just call it when traversing the map.

TEST_VECTORS = [
    (-1, 0), (0, -1), (1, 0), (0, 1)
]


def get_others(map_, r, c) -> int:
    """Go through the map and check the size of the island
       (= summing up all the 1s that are part of the island)

       Input - the map, row, column position
       Output - return the total number)
    """
    nums = 0
    if map_[r][c] == 1:
        for x, y in TEST_VECTORS:
            if r + y < 0 or r + y >= len(map_) or c + x < 0 or c + x >= len(map_[0]):
                nums += 1
            elif map_[r + y][c + x] == 0:
                nums += 1

    return nums


def island_size(map_) -> int:
    """Hint: use the get_others helper

    Input: the map
    Output: the perimeter of the island
    """
    perimeter = sum(get_others(map_, y, x) for y, row in enumerate(map_) for x in range(len(row)))

    return perimeter
