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
        # Not(Black_A and Black_B) <=> Not(Not A and Not B) <=> A or B
        for r in range(rows):
            for c in range(cols):
                if r + 1 < rows:
                    self._model.AddBoolOr([self._grid_vars[r][c], self._grid_vars[r+1][c]])
                if c + 1 < cols:
                    self._model.AddBoolOr([self._grid_vars[r][c], self._grid_vars[r][c+1]])

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

                # Edge case: All black (empty white shapes). Valid only if grid is empty or similar?
                # Usually Hitori has solution. If white_shapes is empty, it means all cells are black.
                # But constraints (no adjacent black) usually prevent all black for grids >= 2x2.

                if not white_shapes:
                     # This shouldn't happen for valid puzzles > 1x1 due to "no adjacent black" rule.
                     # But if it does, it's technically "connected" (0 components).
                     # However, usually we want non-empty solution.
                     # But let's assume it's valid if it satisfies other constraints.
                     # Actually, get_all_shapes returns connected components of True values.
                     pass

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

                    if not valid_around:
                        # This should not happen if not connected to biggest, unless fully enclosed by borders?
                        # If fully enclosed by borders, it's impossible to connect?
                        # Wait, around_shape considers grid boundaries.
                        # If valid_around is empty, it means the shape covers the whole grid? No.
                        # It means it's surrounded by borders. So it IS the whole grid (or max fit).
                        # But we know there is another shape (biggest). So this case implies disconnected components separated by black,
                        # and this component touches borders on all non-black sides?
                        # Actually valid_around are the positions in the grid that are neighbors.
                        # If they are all black (current solution), we force one to be White.
                        pass

                    # Constraint: sum(vars[p] for p in valid_around) >= 1
                    # i.e. AddBoolOr
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
        # We can enforce that at least one cell changes state.
        # However, typically we want to forbid the exact set of Black cells?
        # Or just "not this assignment".
        # Assignment is defined by _grid_vars.

        # Previous solution boolean map
        prev_bools = [[bool(self._previous_solution.value(r,c)) for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)]

        # Constraint: It is NOT the case that (All vars match prev_bools)
        # matches = []
        # for r in... for c in...
        #    if prev_bools[r][c]: matches.append(var)
        #    else: matches.append(Not(var))
        # Add(And(matches).OnlyOne() == False) -> Add(Not(And(matches))) -> Add(Or(Not(m) for m in matches))

        diff_literals = []
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number):
                if prev_bools[r][c]:
                    # Was White (True). To differ, it must be Black (False) -> Not(var)
                    diff_literals.append(self._grid_vars[r][c].Not())
                else:
                    # Was Black (False). To differ, it must be White (True) -> var
                    diff_literals.append(self._grid_vars[r][c])

        # At least one literal in diff_literals must be true (i.e. at least one cell differs)
        self._model.AddBoolOr(diff_literals)

        # Reset solver? No, we need to continue with the new constraint.
        # But we are inside the 'get_solution' loop in concept?
        # Re-running the solve loop with the new model constraint.

        # NOTE: self._solver and self._model are stateful.
        # But 'get_solution' recreates them.
        # HitoriSolver typically calls get_solution, then get_other_solution.
        # If I recreate the model in get_other_solution, I lose the learned clauses/cuts?
        # Yes. But the cuts depend on the specific assignment.
        # If I want to find *another* valid connected solution, I should rebuild the model
        # AND add the negation of the previous solution.
        # Re-using the same solver instance would be better but requires the cuts to be valid globally.
        # The cuts (At least one neighbor of component X must be white) ARE globally valid constraints
        # (Component X surrounded by Black is forbidden).
        # So I can just Add constraint and Solve again.

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
             # Should not happen if called after get_solution
             return Grid.empty()


    def _apply_heuristics(self):
        rows = self._grid.rows_number
        cols = self._grid.columns_number

        # 1. Sandwich Rule: A B A => B is White
        # If grid[r][c] == grid[r][c+2], then grid[r][c+1] must be White.
        # (Because if B is Black, A and A must be White (no adj black), but A and A are same number in row -> invalid)
        for r in range(rows):
            for c in range(cols - 2):
                if self._grid.value(r, c) == self._grid.value(r, c + 2):
                    self._model.Add(self._grid_vars[r][c + 1] == True)

        for c in range(cols):
            for r in range(rows - 2):
                if self._grid.value(r, c) == self._grid.value(r + 2, c):
                    self._model.Add(self._grid_vars[r + 1][c] == True)

        # 2. Lonely/Unique Rule: If a number is unique in its row AND column, it must be White?
        # Not necessarily true in all variants, but standard Hitori:
        # If it was Black, it doesn't solve any collision. Does it *need* to be White?
        # Actually, if it's unique in row AND col, shading it is "wasteful" but not strictly forbidden
        # UNLESS it's needed for connectivity. But we can't force it White just because it's unique.
        # Wait, the previous solver had `_if_unique_in_row_and_column_then_white`.
        # Is that a valid rule?
        # If a number causes no conflicts, making it black risks disconnecting the grid without benefit.
        # But is it *impossible* for it to be black?
        # In strictly logical Hitori, usually yes, but let's stick to safe deductions.
        # If I have [1 2 3], and 2 is unique. Can 2 be black? Yes, if 1 and 3 need to be separated?
        # No, black cells cannot touch.
        # If 2 is black, 1 and 3 are white.
        # There is no rule forbidding unique numbers from being black.
        # However, most Hitori strategies assume you only shade to resolve conflicts.
        # But for *validity*, it's not a constraint.
        # I will SKIP this heuristic to be safe, unless it was crucial. The previous solver had it.
        # Let's check logic: If X is unique in row and col.
        # Shading X doesn't help Rule 1.
        # Shading X creates a "hole" (Rule 3 risk).
        # Shading X puts constraints on neighbors (Rule 2).
        # It seems strictly suboptimal/dominated to shade it.
        # But is it *invalid*?
        # A valid solution implies all constraints met.
        # If there exists a valid solution where X is black, we shouldn't force it White.
        # Example: 1 2 1. Middle 2 is unique. Left/Right 1s collide.
        # One 1 must be black.
        # Can 2 be black? If 2 is black, 1s must be white -> 1s collide -> Invalid.
        # So if neighbors collide, maybe.
        # But what if 1 2 3. No collisions.
        # Solution: All white.
        # Can 2 be black? [1 Black 3]. Valid?
        # Rule 1: OK. Rule 2: OK. Rule 3: 1 and 3 separated.
        # If 1 and 3 connect elsewhere, it's valid.
        # So strictly speaking, a unique number CAN be black.
        # I will remove that constraint to ensure correctness, as we want *valid* solutions, not just "human-like" ones.
        # OR-Tools is fast enough.

        # 3. Adjacent Pair Rule: A A => Everything else in that row/col with value A is Black.
        # (Because one of the A's must be Black, the other White. So the "White quota" for A in this row is filled by the pair).
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

