from z3 import Int, Solver, Distinct


def solve_makaro(grid, regions):
    rows, cols = len(grid), len(grid[0])
    solver = Solver()

    # Define variables: one integer variable for each cell in the grid
    cells = [[Int(f"cell_{r}_{c}") for c in range(cols)] for r in range(rows)]

    # Constraint: Each cell must contain a number >= 1
    for r in range(rows):
        for c in range(cols):
            solver.add(cells[r][c] >= 1)

    # Group cells by regions
    region_cells = {}
    for r in range(rows):
        for c in range(cols):
            region_id = regions[r][c]
            if region_id not in region_cells:
                region_cells[region_id] = []
            region_cells[region_id].append(cells[r][c])

    # Constraint: Numbers in a region must form a valid sequence (Distinct)
    for region_id, region in region_cells.items():
        region_size = len(region)
        solver.add(Distinct(region))  # All numbers in the region must be distinct
        for cell in region:
            solver.add(cell <= region_size)  # Numbers <= size of the region

    # Constraint: Adjacent cells must have different numbers
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    solver.add(cells[r][c] != cells[nr][nc])

    # Solve the puzzle
    if solver.check() == 'sat':
        model = solver.model()
        result = [[model.evaluate(cells[r][c]).as_long() for c in range(cols)] for r in range(rows)]
        return result
    else:
        raise ValueError("No solution found for the given Makaro puzzle.")


# Example usage
grid = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

regions = [
    [1, 1, 2, 2],
    [1, 1, 2, 3],
    [4, 4, 2, 3],
    [4, 4, 3, 3]
]

solution = solve_makaro(grid, regions)
for row in solution:
    print(row)

