from ortools.sat.python import cp_model
from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator

class HitoriSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self._previous_solution: Grid | None = None
        self._solver = None
        self._model = None
        self._grid_vars = None

    def get_solution(self) -> Grid:
        self._model = cp_model.CpModel()
        rows = self._grid.rows_number
        cols = self._grid.columns_number

        # 1. Variables: True = White (Keep), False = Black (Shade)
        self._grid_vars = [[self._model.NewBoolVar(f'cell_{r}_{c}') for c in range(cols)] for r in range(rows)]

        # 2. Basic Constraints

        # Rule 1: No number appears more than once in a row or column (among White cells).
        # Optimization: Pre-group positions by value for each row/col
        for r in range(rows):
            vals_in_row = {}
            for c in range(cols):
                val = self._grid.value(r, c)
                if val not in vals_in_row: vals_in_row[val] = []
                vals_in_row[val].append(c)
            for val, cs in vals_in_row.items():
                if len(cs) > 1:
                    # At most one of these can be White (True)
                    self._model.AddAtMostOne([self._grid_vars[r][c] for c in cs])

        for c in range(cols):
            vals_in_col = {}
            for r in range(rows):
                val = self._grid.value(r, c)
                if val not in vals_in_col: vals_in_col[val] = []
                vals_in_col[val].append(r)
            for val, rs in vals_in_col.items():
                if len(rs) > 1:
                    self._model.AddAtMostOne([self._grid_vars[r][c] for r in rs])

        # Rule 2: Shaded cells (Black/False) cannot be adjacent.
        # Equivalent: For any adjacent pair, at least one must be White (True).
        for position, _ in self._grid:
            for neighbor in position.neighbors():
                if neighbor in self._grid:
                     # Only add constraint if neighbor is "down" or "right" to avoid duplicates?
                     # Or rely on neighbor iterator order?
                     # Let's just add it. Solver can handle redundant constraints, or we filter.
                     # To avoid duplicates: only add if neighbor > position (e.g. r'>r or c'>c)
                     if neighbor.r > position.r or neighbor.c > position.c:
                        self._model.AddBoolOr([
                            self._grid_vars[position.r][position.c],
                            self._grid_vars[neighbor.r][neighbor.c]
                        ])

        # 3. Heuristics
        self._apply_heuristics()

        # 4. Iterative Solving for Connectivity
        self._solver = cp_model.CpSolver()
        # self._solver.parameters.num_search_workers = 8 # optional

        while True:
            status = self._solver.Solve(self._model)
            if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
                # Construct current grid
                # True = White, False = Black
                # But Grid needs the original value if White, False if Black
                current_solution_data = [[self._solver.BooleanValue(self._grid_vars[r][c]) for c in range(cols)] for r in range(rows)]
                current_grid = Grid([[current_solution_data[r][c] for c in range(cols)] for r in range(rows)]) # Grid of bools for shape detection

                # Check connectivity of True cells
                white_shapes = current_grid.get_all_shapes() # Returns list of sets of positions

                if len(white_shapes) <= 1:
                    # Connected!
                    self._previous_solution = self._get_result_grid(current_solution_data)
                    return self._previous_solution

                # Not connected. Add cuts.
                # Logic: For each disconnected component (except the biggest),
                # at least one neighbor MUST be white to connect it to something else.
                biggest = max(white_shapes, key=len)
                for shape in white_shapes:
                    if shape == biggest: continue

                    around = ShapeGenerator.around_shape(shape)
                    valid_around = [p for p in around if p in self._grid]

                    self._model.AddBoolOr([self._grid_vars[p.r][p.c] for p in valid_around])
            else:
                return Grid.empty()

    def _get_result_grid(self, boolean_grid_data):
         # Map True/False back to Numbers/False
         return Grid([[self._grid.value(r, c) if boolean_grid_data[r][c] else False for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])

    def get_other_solution(self):
        if self._previous_solution is None:
             return Grid.empty()

        # We want a solution that is NOT the same as the previous one.
        prev_bools = [[bool(self._previous_solution.value(r,c)) for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)]

        diff_literals = []
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number):
                if prev_bools[r][c]:
                    # Was White (True). To differ, it must be Black (False) -> Not(var)
                    diff_literals.append(self._grid_vars[r][c].Not())
                else:
                    # Was Black (False). To differ, it must be White (True) -> var
                    diff_literals.append(self._grid_vars[r][c])

        if self._solver and self._model:
            # Add constraint to existing model
             self._model.AddBoolOr(diff_literals)
             # Continue the loop
             while True:
                status = self._solver.Solve(self._model)
                if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
                    rows = self._grid.rows_number
                    cols = self._grid.columns_number
                    current_solution_data = [[self._solver.BooleanValue(self._grid_vars[r][c]) for c in range(cols)] for r in range(rows)]
                    current_grid = Grid([[current_solution_data[r][c] for c in range(cols)] for r in range(rows)])

                    white_shapes = current_grid.get_all_shapes()
                    if len(white_shapes) <= 1:
                        self._previous_solution = self._get_result_grid(current_solution_data)
                        return self._previous_solution

                    biggest = max(white_shapes, key=len)
                    for shape in white_shapes:
                        if shape == biggest: continue
                        around = ShapeGenerator.around_shape(shape)
                        valid_around = [p for p in around if p in self._grid]
                        self._model.AddBoolOr([self._grid_vars[p.r][p.c] for p in valid_around])
                else:
                    return Grid.empty()
        else:
             return Grid.empty()


    def _apply_heuristics(self):
        rows = self._grid.rows_number
        cols = self._grid.columns_number

        # 1. Sandwich Rule: A B A => B is White
        # If grid[r][c] == grid[r][c+2], then grid[r][c+1] must be White.
        # This is strictly index based, keeping for loops is cleaner than mapping positions?
        # But we can iterate.
        # Actually, let's keep simple row/col loops for 1D patterns as it's O(rows*cols) anyway.
        # It's cleaner to read "for r in rows... for c in range(cols-2)" than "for p in grid if p + (0,2) in grid..."

        for r in range(rows):
            for c in range(cols - 2):
                if self._grid.value(r, c) == self._grid.value(r, c + 2):
                    self._model.Add(self._grid_vars[r][c + 1] == True)

        for c in range(cols):
            for r in range(rows - 2):
                if self._grid.value(r, c) == self._grid.value(r + 2, c):
                    self._model.Add(self._grid_vars[r + 1][c] == True)

        # 2. Adjacent Pair Rule: A A => Everything else in that row/col with value A is Black.
        for r in range(rows):
            for c in range(cols - 1):
                if self._grid.value(r, c) == self._grid.value(r, c + 1):
                    val = self._grid.value(r, c)
                    # All OTHER cells in row r with value val must be Black
                    for c2 in range(cols):
                        if c2 != c and c2 != c + 1 and self._grid.value(r, c2) == val:
                            self._model.Add(self._grid_vars[r][c2] == False)

        for c in range(cols):
            for r in range(rows - 1):
                if self._grid.value(r, c) == self._grid.value(r + 1, c):
                    val = self._grid.value(r, c)
                    for r2 in range(rows):
                        if r2 != r and r2 != r + 1 and self._grid.value(r2, c) == val:
                            self._model.Add(self._grid_vars[r2][c] == False)

