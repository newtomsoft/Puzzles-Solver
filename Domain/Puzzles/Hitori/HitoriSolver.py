from ortools.sat.python import cp_model
from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator

class HitoriSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self._model = None
        self._solver = None
        self._cells = []
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()

        # Variables: self._cells[r][c] is True if cell is KEPT (White), False if REMOVED (Black/Shaded)
        self._cells = [[self._model.NewBoolVar(f"cell_{r}_{c}") for c in range(self._grid.columns_number)]
                       for r in range(self._grid.rows_number)]

        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._model is None:
            self._init_solver()

        solution = self._ensure_all_white_connected()
        self._previous_solution = solution
        return solution

    def get_other_solution(self):
        if self._previous_solution is None:
             return self.get_solution()

        # Ban previous solution
        previous_assignment = []
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number):
                val = self._previous_solution.value(r, c)
                is_kept = (val is not False)
                if is_kept:
                    previous_assignment.append(self._cells[r][c].Not())
                else:
                    previous_assignment.append(self._cells[r][c])

        self._model.AddBoolOr(previous_assignment)

        return self.get_solution()

    def _ensure_all_white_connected(self):
        while True:
            status = self._solver.Solve(self._model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                return Grid.empty()

            current_bool_grid = Grid([[self._solver.Value(self._cells[r][c]) == 1
                                       for c in range(self._grid.columns_number)]
                                      for r in range(self._grid.rows_number)])

            white_shapes = current_bool_grid.get_all_shapes()

            if len(white_shapes) <= 1:
                return self.get_solution_grid(current_bool_grid)

            biggest_shape = max(white_shapes, key=len)
            white_shapes.remove(biggest_shape)

            for small_shape in white_shapes:
                around_positions = ShapeGenerator.around_shape(small_shape)
                valid_around = [p for p in around_positions if p in self._grid]

                if valid_around:
                    self._model.AddBoolOr([self._cells[p.r][p.c] for p in valid_around])

    def _add_constraints(self):
        self._add_no_duplicate_constraints()
        self._add_no_adjacent_black_constraints()
        self._add_heuristics()

    def _add_no_duplicate_constraints(self):
        # Rule 1: No number appears more than once in a row or column (unshaded).

        # Rows
        for r in range(self._grid.rows_number):
            value_to_cols = {}
            for c in range(self._grid.columns_number):
                val = self._grid.value(r, c)
                if val not in value_to_cols:
                    value_to_cols[val] = []
                value_to_cols[val].append(c)

            for val, cols in value_to_cols.items():
                if len(cols) > 1:
                    # Optimized: AddAtMostOne
                    self._model.AddAtMostOne([self._cells[r][c] for c in cols])

        # Columns
        for c in range(self._grid.columns_number):
            value_to_rows = {}
            for r in range(self._grid.rows_number):
                val = self._grid.value(r, c)
                if val not in value_to_rows:
                    value_to_rows[val] = []
                value_to_rows[val].append(r)

            for val, rows in value_to_rows.items():
                if len(rows) > 1:
                    # Optimized: AddAtMostOne
                    self._model.AddAtMostOne([self._cells[r][c] for r in rows])

    def _add_no_adjacent_black_constraints(self):
        # Rule 2: Shaded (Black) cells cannot be adjacent horizontally or vertically.
        # At least one of the two adjacent cells must be White.

        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number):
                if c + 1 < self._grid.columns_number:
                    self._model.AddBoolOr([self._cells[r][c], self._cells[r][c+1]])
                if r + 1 < self._grid.rows_number:
                    self._model.AddBoolOr([self._cells[r][c], self._cells[r+1][c]])

    def _add_heuristics(self):
        self._if_sandwiched_by_2_same_number_then_white()
        self._if_2_same_number_adjacent_then_others_black()

    def _if_sandwiched_by_2_same_number_then_white(self):
        # Heuristic: A B A. If A's are same number, B must be White.
        # Reason: If B is Black, A(left) and A(right) must be White (Rule 2).
        # But A and A are duplicates in row. Violation of Rule 1.
        # So B cannot be Black.
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number):
                if 0 < r < self._grid.rows_number - 1:
                    if self._grid.value(r - 1, c) == self._grid.value(r + 1, c):
                        self._model.Add(self._cells[r][c] == 1)

                if 0 < c < self._grid.columns_number - 1:
                    if self._grid.value(r, c - 1) == self._grid.value(r, c + 1):
                        self._model.Add(self._cells[r][c] == 1)

    def _if_2_same_number_adjacent_then_others_black(self):
        # Heuristic: If X X are adjacent.
        # Then all other X in that row/col must be Black.
        # Reason: X X adjacent implies at least one is White? No, at least one is Black.
        # Actually logic:
        # Case 1: X(1) White, X(2) Black.
        # Case 2: X(1) Black, X(2) White.
        # Case 3: X(1) Black, X(2) Black -> Impossible (Rule 2).
        # So exactly one of them is White, or both are White?
        # If both White -> Duplicate. Impossible.
        # So EXACTLY ONE of X(1), X(2) is White.
        # Since exactly one is White, any OTHER X(k) in that row must be Black,
        # because if X(k) is White, we have 2 Whites (X(k) and whichever of X(1)/X(2) is White).

        # Rows
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number - 1):
                val = self._grid.value(r, c)
                if val == self._grid.value(r, c + 1):
                    # Found pair (c, c+1)
                    # Constraint: sum(white[c], white[c+1]) == 1 ? Not necessarily.
                    # Wait, if X X are adjacent. Can both be Black? NO.
                    # Can both be White? NO.
                    # So exactly one is White.
                    # So sum(cells[r][c], cells[r][c+1]) == 1.
                    # This is a strong constraint itself!
                    self._model.Add(self._cells[r][c] + self._cells[r][c+1] == 1)

                    # Also force all others to be Black
                    for c_other in range(self._grid.columns_number):
                        if c_other != c and c_other != c + 1:
                            if self._grid.value(r, c_other) == val:
                                self._model.Add(self._cells[r][c_other] == 0)

        # Columns
        for c in range(self._grid.columns_number):
            for r in range(self._grid.rows_number - 1):
                val = self._grid.value(r, c)
                if val == self._grid.value(r + 1, c):
                    # Found pair (r, r+1)
                    self._model.Add(self._cells[r][c] + self._cells[r+1][c] == 1)

                    for r_other in range(self._grid.rows_number):
                        if r_other != r and r_other != r + 1:
                            if self._grid.value(r_other, c) == val:
                                self._model.Add(self._cells[r_other][c] == 0)

    def get_solution_grid(self, proposition_grid: Grid):
        return Grid([[self._grid.value(r, c) if proposition_grid.value(r, c) else False
                      for c in range(self._grid.columns_number)]
                     for r in range(self._grid.rows_number)])
