from z3 import *
from Domain.Puzzles.GameSolver import GameSolver
from Domain.Board.Grid import Grid

class KurodokoSolver(GameSolver):
    def __init__(self):
        super().__init__()
        self.solution_grid = None

    def solve(self, grid: Grid):
        rows = grid.rows_number
        cols = grid.columns_number
        solver = Solver()

        # 0 = Black, 1 = White
        cells = [[Int(f"cell_{r}_{c}") for c in range(cols)] for r in range(rows)]

        for r in range(rows):
            for c in range(cols):
                solver.add(Or(cells[r][c] == 0, cells[r][c] == 1))

                # Numbered cells are white (1)
                val = grid.matrix[r][c]
                if val > 0:
                    solver.add(cells[r][c] == 1)

                    # Visibility Constraint
                    # The number is the count of visible white cells in 4 directions + itself.
                    # Since itself is 1, visible in 4 directions sum + 1 = val

                    terms = [1] # itself

                    # Up
                    for k in range(1, r + 1):
                        cond = And(*[cells[r-i][c] == 1 for i in range(1, k + 1)])
                        terms.append(If(cond, 1, 0))

                    # Down
                    for k in range(1, rows - r):
                        cond = And(*[cells[r+i][c] == 1 for i in range(1, k + 1)])
                        terms.append(If(cond, 1, 0))

                    # Left
                    for k in range(1, c + 1):
                        cond = And(*[cells[r][c-i] == 1 for i in range(1, k + 1)])
                        terms.append(If(cond, 1, 0))

                    # Right
                    for k in range(1, cols - c):
                        cond = And(*[cells[r][c+i] == 1 for i in range(1, k + 1)])
                        terms.append(If(cond, 1, 0))

                    solver.add(Sum(terms) == val)

        # Adjacency Rule: No two black cells are adjacent (horizontally or vertically)
        for r in range(rows):
            for c in range(cols):
                if r + 1 < rows:
                    solver.add(Not(And(cells[r][c] == 0, cells[r+1][c] == 0)))
                if c + 1 < cols:
                    solver.add(Not(And(cells[r][c] == 0, cells[r][c+1] == 0)))

        # Connectivity Rule: All white cells are connected.
        root_r, root_c = -1, -1
        for r in range(rows):
            for c in range(cols):
                if grid.matrix[r][c] > 0:
                    root_r, root_c = r, c
                    break
            if root_r != -1:
                break

        if root_r != -1:
            dist = [[Int(f"dist_{r}_{c}") for c in range(cols)] for r in range(rows)]

            for r in range(rows):
                for c in range(cols):
                    solver.add(If(cells[r][c] == 0, dist[r][c] == -1, dist[r][c] >= 0))

                    if r == root_r and c == root_c:
                        solver.add(If(cells[r][c] == 1, dist[r][c] == 0, True))
                    else:
                        neighbors = []
                        if r > 0: neighbors.append(dist[r-1][c])
                        if r < rows - 1: neighbors.append(dist[r+1][c])
                        if c > 0: neighbors.append(dist[r][c-1])
                        if c < cols - 1: neighbors.append(dist[r][c+1])

                        valid_neighbors_conditions = []
                        for n_dist in neighbors:
                            valid_neighbors_conditions.append(And(n_dist >= 0, dist[r][c] == n_dist + 1))

                        if valid_neighbors_conditions:
                            solver.add(If(cells[r][c] == 1, Or(*valid_neighbors_conditions), True))
                        else:
                            # If no neighbors (e.g. 1x1 grid), but root was found, this condition is trivially true if it is root.
                            # If not root and no neighbors, it can't be white unless it's root.
                            pass

        if solver.check() == sat:
            model = solver.model()
            result_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
            for r in range(rows):
                for c in range(cols):
                    if model[cells[r][c]].as_long() == 1:
                        # Return number if it was number, else 1
                        result_matrix[r][c] = grid.matrix[r][c] if grid.matrix[r][c] > 0 else 1
                    else:
                        result_matrix[r][c] = 0 # Black

            self.solution_grid = Grid(result_matrix)
            return self.solution_grid
        else:
            raise Exception("No solution found")

    def get_solution(self) -> Grid:
        return self.solution_grid

    def get_other_solution(self) -> Grid:
        # Not implementing multiple solutions logic for now
        return self.solution_grid
