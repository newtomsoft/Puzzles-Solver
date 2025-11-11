from typing import Callable

from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class NumberCrossSolver(GameSolver):
    black_value = False  # must stay False
    empty = None  # must stay None

    def __init__(self, input_grid: Grid, row_sums_clues: list, column_sums_clues: list):
        self._input_grid = input_grid
        if self._input_grid.rows_number != self._input_grid.columns_number:
            raise ValueError("The grid must be square")
        self.rows_number = self._input_grid.rows_number
        self.columns_number = self._input_grid.columns_number
        self._row_sums_clues = row_sums_clues
        self._column_sums_clues = column_sums_clues
        self._model = cp_model.CpModel()
        self._grid_vars: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_vars = Grid([[self._model.NewBoolVar(f"cell_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constrains()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()
        if self._previous_solution.is_empty():
            return Grid.empty()

        diff_bools = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                prev_val = 1 if self._previous_solution.value(r, c) != self.black_value else 0
                v = self._grid_vars[Position(r, c)]
                diff = self._model.NewBoolVar(f"diff_{r}_{c}")
                self._model.Add(v != prev_val).OnlyEnforceIf(diff)
                self._model.Add(v == prev_val).OnlyEnforceIf(diff.Not())
                diff_bools.append(diff)
        self._model.AddBoolOr(diff_bools)
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        solver = cp_model.CpSolver()
        status = solver.Solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()
        grid = Grid([
            [self._input_grid[Position(i, j)] if solver.Value(self._grid_vars[Position(i, j)]) == 1 else self.black_value for j in range(self.columns_number)]
            for i in range(self.rows_number)
        ])
        return grid

    def _add_constrains(self):
        self._add_initials_constraints()
        self._add_sums_clues_constraints()

    def _add_initials_constraints(self):
        for position, value in self._input_grid:
            if value == self.black_value:
                self._model.Add(self._grid_vars[position] == 0)

    def _add_sums_clues_constraints(self):
        self._add_constraints_for_clues(self._row_sums_clues, self._row_positions_generator)
        self._add_constraints_for_clues(self._column_sums_clues, self._column_positions_generator)

    def _add_constraints_for_clues(self, clues: list, line_positions_generator: Callable):
        for index, clue in enumerate(clues):
            if clue != self.empty:
                line_positions = line_positions_generator(index)
                self._add_sum_for_line_constraint(line_positions, clue)

    def _row_positions_generator(self, row_index: int) -> list:
        return [Position(row_index, c) for c in range(self.columns_number)]

    def _column_positions_generator(self, column_index: int) -> list:
        return [Position(r, column_index) for r in range(self.rows_number)]

    def _add_sum_for_line_constraint(self, line_positions: list, clue: int):
        self._model.Add(sum((self._input_grid[position] * self._grid_vars[position] for position in line_positions)) == clue)
