from z3 import Solver, Bool, unsat

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class KakurasuSolver(GameSolver):
    def __init__(self, numbers_by_top_left: dict[str, list[int]]):
        self._numbers_side = numbers_by_top_left['side']
        self._numbers_top = numbers_by_top_left['top']
        self.rows_number = len(self._numbers_side)
        self.columns_number = len(self._numbers_top)
        if self.rows_number < 4 or self.columns_number < 4:
            raise ValueError("Kakurasu grid must at least 4x4")
        self._solver = Solver()
        self._grid_z3: list[list[Bool]] = [[]]
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3: list[list[Bool]] = [[Bool(f"matrix_{r}{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._add_constraints()
        if self._solver.check() == unsat:
            return Grid.empty()

        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()

        from z3 import Or
        current_solution_constraints = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                val = self._previous_solution[r][c]
                if val:
                    current_solution_constraints.append(self._grid_z3[r][c] == False)
                else:
                    current_solution_constraints.append(self._grid_z3[r][c] == True)

        self._solver.add(Or(*current_solution_constraints))
        if self._solver.check() == unsat:
            return Grid.empty()

        self._previous_solution = self._compute_solution()
        return self._previous_solution

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
        constraint = sum([self._grid_z3[index][i_column] * (i_column + 1) for i_column in range(self.columns_number)]) == number
        return constraint

    def _add_constraint_sum_column(self, index: int, number: int):
        return sum([self._grid_z3[i_row][index] * (i_row + 1) for i_row in range(self.rows_number)]) == number
