from typing import Any
from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class SummandumSolver(GameSolver):
    cell_empty = None

    def __init__(self, grid: Grid):
        super().__init__()
        self.rows_number = len(grid.matrix)
        self.columns_number = len(grid.matrix[0]) if self.rows_number > 0 else 0
        self._clues = {}
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                p = Position(r, c)
                val = grid[p]
                if val is not self.cell_empty:
                    self._clues[p] = val

        self._model = None
        self._row_vars = None
        self._col_vars = None
        self._header_vars = None  # For row and column headers
        self._status = None

    def _init_model(self):
        self._model = cp_model.CpModel()
        # Headers must be a permutation of 0..N-1
        max_header_value = self.rows_number - 1
        self._row_headers = [self._model.new_int_var(0, max_header_value, f"row_header_{r}") for r in range(self.rows_number)]
        self._col_headers = [self._model.new_int_var(0, max_header_value, f"col_header_{c}") for c in range(self.columns_number)]
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._model is None:
            self._init_model()

        self._status = self._solver.solve(self._model)
        if self._status == cp_model.OPTIMAL or self._status == cp_model.FEASIBLE:
            return self._compute_solution()

        return Grid.empty()

    def get_other_solution(self) -> Grid:
        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return self.get_solution()

        prev_row_values = [self._solver.value(self._row_headers[r]) for r in range(self.rows_number)]
        prev_col_values = [self._solver.value(self._col_headers[c]) for c in range(self.columns_number)]

        row_diff_vars = [self._model.new_bool_var(f"row_diff_{r}") for r in range(self.rows_number)]
        col_diff_vars = [self._model.new_bool_var(f"col_diff_{c}") for c in range(self.columns_number)]

        for r in range(self.rows_number):
            self._model.add(self._row_headers[r] != prev_row_values[r]).only_enforce_if(row_diff_vars[r])

        for c in range(self.columns_number):
            self._model.add(self._col_headers[c] != prev_col_values[c]).only_enforce_if(col_diff_vars[c])

        self._model.add_bool_or(row_diff_vars + col_diff_vars)

        new_status = self._solver.solve(self._model)
        if new_status == cp_model.OPTIMAL or new_status == cp_model.FEASIBLE:
            self._status = new_status
            return self._compute_solution()

        return Grid.empty()

    def _compute_solution(self) -> Grid:
        solution_size = self.rows_number + 1
        solution_matrix = [[self.cell_empty] * solution_size for _ in range(solution_size)]

        for c in range(self.columns_number):
            solution_matrix[0][c + 1] = self._solver.value(self._col_headers[c])

        for r in range(self.rows_number):
            solution_matrix[r + 1][0] = self._solver.value(self._row_headers[r])

        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                if pos in self._clues:
                    solution_matrix[r + 1][c + 1] = self._clues[pos]
                else:
                    solution_matrix[r + 1][c + 1] = self.cell_empty  # Keep empty cells empty

        return Grid(solution_matrix)

    def _add_constraints(self):
        self._add_clues_constraints()
        self._add_unique_constraints()

    def _add_clues_constraints(self):
        for pos, val in self._clues.items():
            self._model.add(self._row_headers[pos.r] + self._col_headers[pos.c] == val)

    def _add_unique_constraints(self):
        self._model.add_all_different(self._row_headers)
        self._model.add_all_different(self._col_headers)
