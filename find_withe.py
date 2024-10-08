def find_white(grid):
    rows_number = len(grid)
    columns_number = len(grid[0])
    for i in range(rows_number):
        for j in range(columns_number):
            if grid[i][j]:
                return i, j
    return None, None
