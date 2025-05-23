import math
from abc import abstractmethod

from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver
from Utils.utils import is_perfect_square


class SudokuBaseSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._sub_square_row_number = 0
        self._sub_square_column_number = 0
        if self.rows_number != self.columns_number:
            raise ValueError("Sudoku grid must be square")
        if not self._are_initial_numbers_different_in_row_and_column():
            raise ValueError("Initial numbers must be different in rows and columns")
        if not self._are_initial_numbers_between_1_and_nxn():
            raise ValueError("initial numbers must be between 1 and n x n")
        self._grid_vars = None
        self._model = cp_model.CpModel()
        self._previous_solution: Grid | None = None

    def _init_sub_squares(self):
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

    def get_solution(self) -> (Grid | None, int):
        self._grid_vars = Grid([[self._model.NewIntVar(1, self.rows_number, f"grid_{r}_{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        self._add_constraints()
        self._add_specific_constraints()

        solver = cp_model.CpSolver()
        status = solver.Solve(self._model)

        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return Grid.empty()

        self._previous_solution = Grid([[solver.Value(self._grid_vars.value(i, j)) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return self._previous_solution

    def get_other_solution(self):
        if self._previous_solution is None:
            return self.get_solution()

        bool_vars = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                prev_val = self._previous_solution.value(r, c)
                diff_var = self._model.NewBoolVar(f"diff_r{r}_c{c}")
                self._model.Add(self._grid_vars[Position(r, c)] != prev_val).OnlyEnforceIf(diff_var)
                self._model.Add(self._grid_vars[Position(r, c)] == prev_val).OnlyEnforceIf(diff_var.Not())
                bool_vars.append(diff_var)

        self._model.AddBoolOr(bool_vars)

        return self.get_solution()

    def _add_constraints(self):
        self._initials_constraints()
        self._add_distinct_in_rows_and_columns_constraints()

    @abstractmethod
    def _add_specific_constraints(self):
        pass

    def _initials_constraints(self):
        for position, value in [(position, value) for position, value in self._grid if value != -1]:
            self._model.Add(self._grid_vars[position] == value)

    def _add_distinct_in_rows_and_columns_constraints(self):
        for r in range(self.rows_number):
            self._model.AddAllDifferent([self._grid_vars[Position(r, c)] for c in range(self.columns_number)])
        for c in range(self.columns_number):
            self._model.AddAllDifferent([self._grid_vars[Position(r, c)] for r in range(self.rows_number)])

    def _add_distinct_in_sub_squares_constraints(self):
        for sub_square_row in range(0, self.rows_number, self._sub_square_row_number):
            for sub_square_column in range(0, self.columns_number, self._sub_square_column_number):
                cells = []
                for r in range(self._sub_square_row_number):
                    for c in range(self._sub_square_column_number):
                        cells.append(self._grid_vars.value(sub_square_row + r, sub_square_column + c))
                self._model.AddAllDifferent(cells)

    def _are_initial_numbers_different_in_row_and_column(self):
        seen_in_rows = [set() for _ in range(self.rows_number)]
        seen_in_columns = [set() for _ in range(self.columns_number)]
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                value = self._grid.value(r, c)
                if value == -1:
                    continue
                if value in seen_in_rows[r] or value in seen_in_columns[c]:
                    return False
                seen_in_rows[r].add(value)
                seen_in_columns[c].add(value)
        return True

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

    def _are_initial_numbers_between_1_and_nxn(self):
        return all(
            self._grid.value(r, c) == -1 or 1 <= self._grid.value(r, c) <= self.rows_number
            for r in range(self.rows_number)
            for c in range(self.columns_number)
        )
