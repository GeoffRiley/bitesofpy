from collections import deque


def count_islands(grid):
    """
    Input: 2D matrix, each item is [x, y] -> row, col.
    Output: number of islands, or 0 if found none.
    Notes: island is denoted by 1, ocean by 0 islands is counted by continously
        connected vertically or horizontically  by '1's.
    It's also preferred to check/mark the visited islands:
    - eg. using the helper function - mark_islands().
    """
    islands = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 1:
                islands += 1
                mark_islands(r, c, grid)
    return islands


def check_grid(i, j, grid):
    """

    :param i:   Row to examine
    :param j:   Col to examine
    :param grid: Grid
    :return: Boolean for island present or not
    """
    # first get rid of edge cases
    if i < 0 or j < 0 or i >= len(grid) or j >= len(grid[0]):
        return False
    return grid[i][j] != 0


VECTORS = [(-1, 0), (0, -1), (1, 0), (0, 1)]


def mark_islands(i, j, grid):
    """
    Input: the row, column and grid
    Output: None. Just mark the visisted islands as in-place operation.
    """
    queue = deque([(i, j)])
    while len(queue) > 0:
        y, x = queue.popleft()
        grid[y][x] = 0  # sink the island!
        # now look around it…
        for yo, xo in VECTORS:
            if check_grid(y + yo, x + xo, grid):
                queue.append((y + yo, x + xo))
