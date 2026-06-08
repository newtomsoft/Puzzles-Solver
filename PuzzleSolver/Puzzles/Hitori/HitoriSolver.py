from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class HitoriSolver(GameSolver):
    def __init__(self, grid: Grid):
        super().__init__()
        self._grid = grid
        self._model = cp_model.CpModel()
        self._grid_vars = None
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_vars = Grid([[self._model.new_bool_var(f"grid_{r}_{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._grid_vars is None:
            self._init_solver()

        status = self._solver.solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        boolean_grid = self._build_boolean_grid_from_solution()
        solution = self._build_solution_grid(boolean_grid)
        self._previous_solution = solution
        return solution

    def get_other_solution(self):
        if self._previous_solution is None:
            return self.get_solution()

        previous_black_cells = [pos for pos, val in self._previous_solution if not val]
        self._model.add_bool_or([self._grid_vars[p] for p in previous_black_cells])
        return self.get_solution()

    def _build_boolean_grid_from_solution(self):
        return Grid([[self._solver.boolean_value(self._grid_vars[r][c]) for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])

    def _build_solution_grid(self, boolean_grid):
        return Grid([[self._grid.value(r, c) if boolean_grid.value(r, c) else False for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])

    def _add_constraints(self):
        self._add_no_adjacent_black_cells_constraint()
        self._add_no_duplicate_numbers_in_rows_constraint()
        self._add_no_duplicate_numbers_in_columns_constraint()
        self._add_unique_number_in_row_and_column_must_be_white_constraint()
        self._add_three_consecutive_identical_constraint()
        self._add_one_between_identical_constraint()
        self._add_white_connectivity_constraint()

    def _add_white_connectivity_constraint(self):
        total_cells = self._grid.rows_number * self._grid.columns_number
        self._rank_vars = Grid([[self._model.new_int_var(0, total_cells - 1, f"rank_{r}_{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        is_root_vars = []
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number):
                pos = Position(r, c)
                is_root = self._model.new_bool_var(f"is_root_{r}_{c}")
                is_root_vars.append(is_root)
                is_white = self._grid_vars[pos]
                self._model.add(is_root <= is_white)
                self._model.add(self._rank_vars[pos] == 0).OnlyEnforceIf(is_root)
        self._model.add(sum(is_root_vars) == 1)
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number):
                pos = Position(r, c)
                is_white = self._grid_vars[pos]
                is_root = is_root_vars[r * self._grid.columns_number + c]
                parent_literals = []
                for neighbor in self._grid_vars.neighbors_positions(pos):
                    parent = self._model.new_bool_var(f"parent_{r}_{c}_{neighbor.r}_{neighbor.c}")
                    self._model.add(self._grid_vars[neighbor] == 1).OnlyEnforceIf(parent)
                    self._model.add(self._rank_vars[neighbor] < self._rank_vars[pos]).OnlyEnforceIf(parent)
                    parent_literals.append(parent)
                if parent_literals:
                    self._model.add_bool_or(parent_literals).OnlyEnforceIf([is_white, is_root.negated()])

    def _add_no_adjacent_black_cells_constraint(self):
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number):
                if r + 1 < self._grid.rows_number:
                    self._model.add(self._grid_vars[r][c] + self._grid_vars[r + 1][c] >= 1)
                if c + 1 < self._grid.columns_number:
                    self._model.add(self._grid_vars[r][c] + self._grid_vars[r][c + 1] >= 1)

    def _add_no_duplicate_numbers_in_rows_constraint(self):
        for r in range(self._grid.rows_number):
            vals = {}
            for c in range(self._grid.columns_number):
                val = self._grid[r][c]
                if val not in vals:
                    vals[val] = []
                vals[val].append(c)
            for val, cols in vals.items():
                if len(cols) > 1:
                    self._model.add(sum(self._grid_vars[r][c] for c in cols) <= 1)

    def _add_no_duplicate_numbers_in_columns_constraint(self):
        for c in range(self._grid.columns_number):
            vals = {}
            for r in range(self._grid.rows_number):
                val = self._grid[r][c]
                if val not in vals:
                    vals[val] = []
                vals[val].append(r)
            for val, rows in vals.items():
                if len(rows) > 1:
                    self._model.add(sum(self._grid_vars[r][c] for r in rows) <= 1)

    def _add_unique_number_in_row_and_column_must_be_white_constraint(self):
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number):
                val = self._grid[r][c]
                unique_in_row = sum(1 for c2 in range(self._grid.columns_number) if self._grid[r][c2] == val) == 1
                unique_in_col = sum(1 for r2 in range(self._grid.rows_number) if self._grid[r2][c] == val) == 1
                if unique_in_row and unique_in_col:
                    self._model.add(self._grid_vars[r][c] == 1)

    def _add_three_consecutive_identical_constraint(self):
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number - 2):
                if self._grid[r][c] == self._grid[r][c + 1] == self._grid[r][c + 2]:
                    self._model.add(self._grid_vars[r][c + 1] == 1)
                    self._model.add(self._grid_vars[r][c] == 0)
                    self._model.add(self._grid_vars[r][c + 2] == 0)

        for c in range(self._grid.columns_number):
            for r in range(self._grid.rows_number - 2):
                if self._grid[r][c] == self._grid[r + 1][c] == self._grid[r + 2][c]:
                    self._model.add(self._grid_vars[r + 1][c] == 1)
                    self._model.add(self._grid_vars[r][c] == 0)
                    self._model.add(self._grid_vars[r + 2][c] == 0)

    def _add_one_between_identical_constraint(self):
        for r in range(self._grid.rows_number):
            for c in range(self._grid.columns_number - 2):
                if self._grid[r][c] == self._grid[r][c + 2]:
                    self._model.add(self._grid_vars[r][c + 1] == 1)

        for c in range(self._grid.columns_number):
            for r in range(self._grid.rows_number - 2):
                if self._grid[r][c] == self._grid[r + 2][c]:
                    self._model.add(self._grid_vars[r + 1][c] == 1)
