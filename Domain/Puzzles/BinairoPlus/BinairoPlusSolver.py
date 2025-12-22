from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class BinairoPlusSolver(GameSolver):
    def __init__(self, grid: Grid, comparisons_positions: dict):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number % 2 != 0:
            raise ValueError("The grid size must be even")

        self._comparisons_positions = comparisons_positions

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
            return Grid.empty()

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
            return Grid.empty()

        return self._compute_solution()

    def _compute_solution(self) -> Grid:
        grid = Grid([[1 if self._solver.Value(self._grid_vars[i][j]) else 0 for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_half_true_false_by_line_constraints()
        self._add_not_same_3_adjacent_constraints()
        self._add_comparison_operators_constraints()

    def _add_initial_constraints(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._grid.value(r, c) == 0:
                    self._model.Add(self._grid_vars[r][c] == 0)
                elif self._grid.value(r, c) == 1:
                    self._model.Add(self._grid_vars[r][c] == 1)

    def _add_half_true_false_by_line_constraints(self):
        half_columns = self.columns_number // 2
        half_rows = self.rows_number // 2
        for r in range(self.rows_number):
            self._model.Add(sum(self._grid_vars[r][c] for c in range(self.columns_number)) == half_columns)
        for c in range(self.columns_number):
            self._model.Add(sum(self._grid_vars[r][c] for r in range(self.rows_number)) == half_rows)

    def _add_not_same_3_adjacent_constraints(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number - 2):
                self._model.AddLinearConstraint(
                    self._grid_vars[r][c] + self._grid_vars[r][c+1] + self._grid_vars[r][c+2], 1, 2
                )
        for c in range(self.columns_number):
            for r in range(self.rows_number - 2):
                self._model.AddLinearConstraint(
                    self._grid_vars[r][c] + self._grid_vars[r+1][c] + self._grid_vars[r+2][c], 1, 2
                )

    def _add_comparison_operators_constraints(self):
        for position0, position1 in self._comparisons_positions['equal']:
            self._model.Add(self._grid_vars[position0.r][position0.c] == self._grid_vars[position1.r][position1.c])
        for position0, position1 in self._comparisons_positions['non_equal']:
            self._model.Add(self._grid_vars[position0.r][position0.c] != self._grid_vars[position1.r][position1.c])
