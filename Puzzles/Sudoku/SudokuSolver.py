import math

from Ports.SolverEngine import SolverEngine
from Puzzles.GameSolver import GameSolver
from Sudoku.SudokuBaseSolver import SudokuBaseSolver
from Utils.Grid import Grid
from Utils.utils import is_perfect_square


class SudokuSolver(SudokuBaseSolver, GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        super().__init__(grid, solver_engine)
        if not is_perfect_square(self.rows_number) and self.rows_number != 6 and self.rows_number != 12:
            raise ValueError("Sudoku subgrid must have size n x n or 3x2 or 4x3")
        if is_perfect_square(self.rows_number):
            self._sub_square_row_number = int(math.sqrt(self.rows_number))
            self._sub_square_column_number = int(self._sub_square_row_number)
        elif self.rows_number == 6:
            self._sub_square_row_number = 2
            self._sub_square_column_number = 3
        else:
            self._sub_square_row_number = 3
            self._sub_square_column_number = 4
        if not self._are_initial_numbers_different_in_sub_square():
            raise ValueError("initial numbers must be different in sub squares")

    def _are_initial_numbers_different_in_sub_square(self):
        for sub_square_row in range(0, self.rows_number, self._sub_square_row_number):
            for sub_square_column in range(0, self.columns_number, self._sub_square_column_number):
                seen_in_sub_square = set()
                for r in range(self._sub_square_row_number):
                    for c in range(self._sub_square_column_number):
                        value = self._grid.value(sub_square_row + r, sub_square_column + c)
                        if value == -1:
                            continue
                        if value in seen_in_sub_square:
                            return False
                        seen_in_sub_square.add(value)
        return True

    def _add_specific_constraints(self):
        self._add_distinct_in_sub_squares_constraints()

    def _add_distinct_in_sub_squares_constraints(self):
        for sub_square_row in range(0, self.rows_number, self._sub_square_row_number):
            for sub_square_column in range(0, self.columns_number, self._sub_square_column_number):
                for r in range(self._sub_square_row_number):
                    for c in range(self._sub_square_column_number):
                        constraint = self._solver.distinct(
                            [self._grid_z3.value(sub_square_row + r, sub_square_column + c) for c in range(self._sub_square_column_number) for r in range(self._sub_square_row_number)]
                        )
                        self._solver.add(constraint)
