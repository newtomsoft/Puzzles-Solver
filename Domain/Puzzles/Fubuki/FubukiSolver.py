import math
from abc import abstractmethod

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Ports.SolverEngine import SolverEngine
from Domain.Puzzles.GameSolver import GameSolver
from Utils.utils import is_perfect_square


class FubukiSolver(GameSolver):
    def __init__(self, grid: Grid, row_sums:list[int], column_sums:list[int], solver_engine: SolverEngine):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self.row_sums = row_sums
        self.column_sums = column_sums
        self._sub_square_row_number = 0
        self._sub_square_column_number = 0
        if self.rows_number != 3  or self.rows_number != self.columns_number:
            raise ValueError("Fubuki grid must be a 3x3 square")
        if not self._verify_initial_numbers_distinct():
            raise ValueError("Initial numbers must be different in rows and columns")
        if not self._verify_initial_numbers_between_1_and_9():
            raise ValueError("initial numbers must be between 1 and 9")
        self._grid_z3 = None
        self._solver = solver_engine
        self._previous_solution: Grid | None = None

    def get_solution(self) -> (Grid | None, int):
        self._grid_z3 = Grid([[self._solver.int(f"grid_{r}_{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        self._add_constraints()
        if not self._solver.has_solution():
            return Grid.empty()
        self._previous_solution = Grid([[self._solver.eval(self._grid_z3.value(i, j)) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return self._previous_solution

    def get_other_solution(self):
        constraints = []
        for position, value in self._previous_solution:
            constraints.append(self._grid_z3[position] == value)
        self._solver.add(self._solver.Not(self._solver.And(constraints)))
        return self.get_solution()

    def _add_constraints(self):
        self._initials_constraints()
        self._add_distinct_constraints()
        self._add_sums_constraints()

    def _initials_constraints(self):
        for position, value in self._grid:
            if value != -1:
                self._solver.add(self._grid_z3[position] == value)
            else:
                self._solver.add(self._grid_z3[position] >= 1)
                self._solver.add(self._grid_z3[position] <= 9)

    def _add_distinct_constraints(self):
        self._solver.add(self._solver.distinct([grid_z3_value for _, grid_z3_value in self._grid_z3]))

    def _add_sums_constraints(self):
        for r in range(self.rows_number):
            self._solver.add(self._solver.sum([self._grid_z3[Position(r, c)] for c in range(self.columns_number)]) == self.row_sums[r])
        for c in range(self.columns_number):
            self._solver.add(self._solver.sum([self._grid_z3[Position(r, c)] for r in range(self.rows_number)]) == self.column_sums[c])

    def _verify_initial_numbers_distinct(self) -> bool:
        initial_numbers = [value for position, value in self._grid if value != -1]
        return len(initial_numbers) == len(set(initial_numbers))

    def _verify_initial_numbers_between_1_and_9(self):
        return all(
            self._grid.value(r, c) == -1 or 1 <= self._grid.value(r, c) <= 9
            for r in range(self.rows_number)
            for c in range(self.columns_number)
        )
