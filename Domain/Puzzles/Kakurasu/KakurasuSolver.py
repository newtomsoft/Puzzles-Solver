from typing import Any, List, Union

from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class KakurasuSolver(GameSolver):
    empty = None

    def __init__(self, data_or_grid: Union[Grid, dict[str, List[int]]]):
        if isinstance(data_or_grid, Grid):
            self._grid = data_or_grid
            self.rows_number = self._grid.rows_number
            self.columns_number = self._grid.columns_number
            self._rows_targets = [self._grid.value(r, self.columns_number - 1) for r in range(self.rows_number)]
            self._columns_targets = [self._grid.value(self.rows_number - 1, c) for c in range(self.columns_number)]
        elif isinstance(data_or_grid, dict):
            self._rows_targets = data_or_grid['side']
            self._columns_targets = data_or_grid['top']
            self.rows_number = len(self._rows_targets)
            self.columns_number = len(self._columns_targets)
            self._grid = None
        else:
             raise ValueError("Input must be Grid or dict")

        if self.rows_number < 4 or self.columns_number < 4:
            raise ValueError("Kakurasu grid must at least 4x4")

        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")

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
        self._add_rows_constraints()
        self._add_columns_constraints()

    def _add_rows_constraints(self):
        for r in range(self.rows_number):
            target = self._rows_targets[r]
            if target != self.empty:
                self._model.Add(sum([(c + 1) * self._grid_vars[r][c] for c in range(self.columns_number)]) == target)

    def _add_columns_constraints(self):
        for c in range(self.columns_number):
            target = self._columns_targets[c]
            if target != self.empty:
                self._model.Add(sum([(r + 1) * self._grid_vars[r][c] for r in range(self.rows_number)]) == target)
