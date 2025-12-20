from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class SumpleteSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number

        # Test `test_solution_grid_square` (2x3) expects "The grid must be square" (FAIL: got "at least 3x3")
        # Test `test_solution_grid_size_less_than_2` (2x2) expects "Sumplete grid (without sums) must be at least 2x2" (FAIL: got "at least 3x3")

        # So I must check square first.
        if self.rows_number != self.columns_number:
            raise ValueError("Sumplete grid must be square") # Changed message to match old test expectation if possible, or new one?
            # Test expects "Sumplete grid must be square".

        # Then check size.
        # Test 2x2 grid -> Error.
        # 3x3 grid -> OK (test_solution_3x3).
        # So min size is 3 (1x1 puzzle + targets).
        if self.rows_number < 3:
             # Test expected: "Sumplete grid (without sums) must be at least 2x2"
             raise ValueError("Sumplete grid (without sums) must be at least 2x2")

        self._target_rows = [self._grid.value(r, self.columns_number - 1) for r in range(self.rows_number)]
        self._target_columns = [self._grid.value(self.rows_number - 1, c) for c in range(self.columns_number)]
        self._model = None
        self._solver = cp_model.CpSolver()
        self._grid_vars = None
        self._status = None

    def _init_model(self):
        self._model = cp_model.CpModel()
        self._grid_vars = [[self._model.NewBoolVar(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._model is None:
            self._init_model()

        self._status = self._solver.Solve(self._model)

        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return None

        return self._compute_solution()

    def get_other_solution(self) -> Grid:
        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return self.get_solution()

        current_vars = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                var = self._grid_vars[r][c]
                if self._solver.BooleanValue(var):
                    current_vars.append(var.Not())
                else:
                    current_vars.append(var)
        self._model.AddBoolOr(current_vars)

        self._status = self._solver.Solve(self._model)

        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return None

        return self._compute_solution()

    def _compute_solution(self) -> Grid:
        # Return N-1 x N-1 grid of Booleans
        grid = Grid([[True if self._solver.Value(self._grid_vars[i][j]) else False
                      for j in range(self.columns_number - 1)]
                     for i in range(self.rows_number - 1)])
        return grid

    def _add_constraints(self):
        self._add_rows_constraints()
        self._add_columns_constraints()

    def _add_rows_constraints(self):
        for r in range(self.rows_number - 1):
            self._model.Add(sum([self._grid.value(r, c) * self._grid_vars[r][c] for c in range(self.columns_number - 1)]) == self._target_rows[r])

    def _add_columns_constraints(self):
        for c in range(self.columns_number - 1):
            self._model.Add(sum([self._grid.value(r, c) * self._grid_vars[r][c] for r in range(self.rows_number - 1)]) == self._target_columns[c])
