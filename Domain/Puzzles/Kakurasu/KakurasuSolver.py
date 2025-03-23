from z3 import Bool

from Domain.Grid.Grid import Grid
from GameSolver import GameSolver
from Ports.SolverEngine import SolverEngine


class KakurasuSolver(GameSolver):
    def __init__(self, numbers_by_top_left: dict[str, list[int]], solver_engine: SolverEngine):
        self._numbers_side = numbers_by_top_left['side']
        self._numbers_top = numbers_by_top_left['top']
        self.rows_number = len(self._numbers_side)
        self.columns_number = len(self._numbers_top)
        if self.rows_number < 4 or self.columns_number < 4:
            raise ValueError("Kakurasu grid must at least 4x4")
        self._solver = solver_engine
        self._grid_z3: list[list[Bool]] = [[]]

    def get_solution(self) -> Grid:
        self._grid_z3: list[list[Bool]] = [[Bool(f"matrix_{r}{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._add_constraints()
        if not self._solver.has_solution():
            return Grid.empty()

        return self._compute_solution()

    def get_other_solution(self) -> Grid:
        raise NotImplemented("This method is not yet implemented")

    def _compute_solution(self):
        model = self._solver.model()
        solution = [[bool(model.eval(self._grid_z3[r][c])) for c in range(self.columns_number)] for r in range(self.rows_number)]
        return Grid(solution)

    def _add_constraints(self):
        for row_index in range(self.rows_number):
            self._solver.add(self._add_constraint_sum_row(row_index, self._numbers_side[row_index]))
        for column_index in range(self.columns_number):
            self._solver.add(self._add_constraint_sum_column(column_index, self._numbers_top[column_index]))

    def _add_constraint_sum_row(self, index: int, number: int):
        constraint = self._solver.sum([self._grid_z3[index][i_column] * (i_column + 1) for i_column in range(self.columns_number)]) == number
        return constraint

    def _add_constraint_sum_column(self, index: int, number: int):
        return self._solver.sum([self._grid_z3[i_row][index] * (i_row + 1) for i_row in range(self.rows_number)]) == number
