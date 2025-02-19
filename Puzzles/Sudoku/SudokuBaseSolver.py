from abc import abstractmethod

from Ports.SolverEngine import SolverEngine
from Puzzles.GameSolver import GameSolver
from Utils.Grid import Grid


class SudokuBaseSolver(GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("Sudoku grid must be square")
        if not self._are_initial_numbers_different_in_row_and_column():
            raise ValueError("Initial numbers must be different in rows and columns")
        if not self._are_initial_numbers_between_1_and_nxn():
            raise ValueError("initial numbers must be between 1 and n x n")
        self._grid_z3 = None
        self._solver = solver_engine

    def get_solution(self) -> (Grid | None, int):
        self._grid_z3 = Grid([[self._solver.int(f"grid_{r}_{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        self._add_constraints()
        self._add_specific_constraints()
        if not self._solver.has_solution():
            return None
        grid = Grid([[self._solver.eval(self._grid_z3.value(i, j)) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def _add_constraints(self):
        self._initials_constraints()
        self._add_distinct_in_rows_and_columns_constraints()

    def _initials_constraints(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._grid.value(r, c) == -1:
                    self._solver.add(self._grid_z3.value(r, c) >= 1)
                    self._solver.add(self._grid_z3.value(r, c) <= self.rows_number)
                else:
                    self._solver.add(self._grid_z3.value(r, c) == self._grid.value(r, c))

    def _add_distinct_in_rows_and_columns_constraints(self):
        for r in range(self.rows_number):
            self._solver.add(self._solver.distinct([self._grid_z3.value(r, c) for c in range(self.columns_number)]))
        for c in range(self.columns_number):
            self._solver.add(self._solver.distinct([self._grid_z3.value(r, c) for r in range(self.rows_number)]))

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

    def _are_initial_numbers_between_1_and_nxn(self):
        return all(
            self._grid.value(r, c) == -1 or 1 <= self._grid.value(r, c) <= self.rows_number
            for r in range(self.rows_number)
            for c in range(self.columns_number)
        )

    @abstractmethod
    def _add_specific_constraints(self):
        pass
