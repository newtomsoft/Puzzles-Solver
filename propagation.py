from find_withe import find_white


def propagation(grid):
    rows_number = len(grid)
    columns_number = len(grid[0])
    right_link = [[False for _ in range(columns_number)] for _ in range(rows_number)]
    down_link = [[False for _ in range(columns_number)] for _ in range(rows_number)]
    left_link = [[False for _ in range(columns_number)] for _ in range(rows_number)]
    up_link = [[False for _ in range(columns_number)] for _ in range(rows_number)]

    for i in range(rows_number):
        for j in range(columns_number):
            if j < columns_number - 1:
                if grid[i][j] and grid[i][j + 1]:
                    right_link[i][j] = True
            if j > 0:
                if grid[i][j] and grid[i][j - 1]:
                    left_link[i][j] = True
            if i < rows_number - 1:
                if grid[i][j] and grid[i + 1][j]:
                    down_link[i][j] = True
            if i > 0:
                if grid[i][j] and grid[i - 1][j]:
                    up_link[i][j] = True

    def dfs(r, c, visited):
        if (grid[r][c] == False) or ((r, c) in visited):
            return visited
        visited.add((r, c))

        # Move right
        if c < columns_number - 1 and (r, c + 1) not in visited:
            if right_link[r][c]:
                new_visited = dfs(r, c + 1, visited)
                if new_visited != visited:
                    return new_visited

        # Move down
        if r < rows_number - 1 and (r + 1, c) not in visited:
            if down_link[r][c]:
                new_visited = dfs(r + 1, c, visited)
                if new_visited != visited:
                    return new_visited

        # Move left
        if c > 0 and (r, c - 1) not in visited:
            if left_link[r][c]:
                new_visited = dfs(r, c - 1, visited)
                if new_visited != visited:
                    return new_visited

        # Move up
        if r > 0 and (r - 1, c) not in visited:
            if up_link[r][c]:
                new_visited = dfs(r - 1, c, visited)
                if new_visited != visited:
                    return new_visited

        return visited

    i0, j0 = find_white(grid)
    if i0 is None:
        return False, set()

    visited_result = dfs(i0, j0, set())
    return len(visited_result) == sum(cell == True for row in grid for cell in row), visited_result


