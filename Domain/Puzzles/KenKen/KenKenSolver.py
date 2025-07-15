import math

from z3 import Solver, Not, And, unsat, Or, Int, Distinct, Abs

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class KenKenSolver(GameSolver):
    def __init__(self, regions_operators_results: list[tuple[list[Position], str, int]]):
        self._regions_operators_results = regions_operators_results
        self.rows_number, self.columns_number = self._get_rows_columns_number()
        if self.rows_number != self.columns_number:
            raise ValueError("KenKen grid must be square")
        self._grid_z3 = None
        self._solver = Solver()
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Int(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        return self._compute_solution()

    def _compute_solution(self) -> Grid:
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        self._previous_solution = Grid([[model.eval(self._grid_z3.value(i, j)).as_long() for j in range(self.columns_number)] for i in range(self.rows_number)])
        return self._previous_solution

    def get_other_solution(self):
        constraints = []
        for position, value in self._previous_solution:
            constraints.append(self._grid_z3[position] == value)
        self._solver.add(Not(And(constraints)))
        return self._compute_solution()

    def _add_constraints(self):
        self._initials_constraints()
        self._add_distinct_in_rows_and_columns_constraints()
        self._add_operations_add_constraints()
        self._add_operations_sub_constraints()
        self._add_operations_mul_constraints()
        self._add_operations_div_constraints()

    def _initials_constraints(self):
        for position, value in self._grid_z3:
            self._solver.add(self._grid_z3[position] >= 1)
            self._solver.add(self._grid_z3[position] <= self.rows_number)

    def _add_distinct_in_rows_and_columns_constraints(self):
        for r in range(self.rows_number):
            self._solver.add(Distinct([self._grid_z3[Position(r, c)] for c in range(self.columns_number)]))
        for c in range(self.columns_number):
            self._solver.add(Distinct([self._grid_z3[Position(r, c)] for r in range(self.rows_number)]))

    def _add_operations_mul_constraints(self):
        for region, _, result in [(region, operator_str, result) for region, operator_str, result in self._regions_operators_results if operator_str == 'x']:
            constraint = math.prod([self._grid_z3[position] for position in region]) == result
            self._solver.add(constraint)

    def _add_operations_div_constraints(self):
        for region, _, result in [(region, operator_str, result) for region, operator_str, result in self._regions_operators_results if operator_str == '÷']:
            if len(region) != 2:
                raise ValueError("Division can only be applied to two positions")
            constraint = Or(
                self._grid_z3[region[0]] * result == self._grid_z3[region[1]],
                self._grid_z3[region[1]] * result == self._grid_z3[region[0]]
            )
            self._solver.add(constraint)

    def _add_operations_add_constraints(self):
        for region, _, result in [(region, operator_str, result) for region, operator_str, result in self._regions_operators_results if operator_str == '+']:
            constraint = sum([self._grid_z3[position] for position in region]) == result
            self._solver.add(constraint)

    def _add_operations_sub_constraints(self):
        for region, _, result in [(region, operator_str, result) for region, operator_str, result in self._regions_operators_results if operator_str == '-']:
            if len(region) != 2:
                raise ValueError("Subtraction can only be applied to two positions")
            constraint = Abs(self._grid_z3[region[0]] - self._grid_z3[region[1]]) == result
            self._solver.add(constraint)

    def _get_rows_columns_number(self) -> tuple[int, int]:
        all_positions = [pos for sublist, _, _ in self._regions_operators_results for pos in sublist]
        min_r = min(pos.r for pos in all_positions)
        max_r = max(pos.r for pos in all_positions)
        min_c = min(pos.c for pos in all_positions)
        max_c = max(pos.c for pos in all_positions)
        return max_r - min_r + 1, max_c - min_c + 1
