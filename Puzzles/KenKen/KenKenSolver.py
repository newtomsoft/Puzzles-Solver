import operator
from functools import reduce
from typing import List, Tuple

from Ports.SolverEngine import SolverEngine
from Puzzles.GameSolver import GameSolver
from Utils.Grid import Grid
from Utils.Position import Position


class KenKenSolver(GameSolver):
    def __init__(self, regions_operators_results: List[Tuple[List[Position], str, int]], solver_engine: SolverEngine):
        # self._regions = [region for region, _, _ in regions_operators_results]
        # self._operators = [operator for _, operator, _ in regions_operators_results]
        # self._results = [result for _, _, result in regions_operators_results]
        self._regions_operators_results = regions_operators_results
        self.rows_number = self._get_rows_number()
        self.columns_number = self._get_columns_number()
        if self.rows_number != self.columns_number:
            raise ValueError("KenKen grid must be square")
        self._grid_z3 = None
        self._solver = solver_engine
        self._previous_solution: Grid | None = None

    def get_solution(self) -> (Grid | None, int):
        self._grid_z3 = Grid([[self._solver.int(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
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
        self._add_distinct_in_rows_and_columns_constraints()
        self._add_results_operations_constraints()

    def _initials_constraints(self):
        for position, value in self._grid_z3:
            self._solver.add(self._grid_z3[position] >= 1)
            self._solver.add(self._grid_z3[position] <= self.rows_number)

    def _add_distinct_in_rows_and_columns_constraints(self):
        for r in range(self.rows_number):
            self._solver.add(self._solver.distinct([self._grid_z3[Position(r, c)] for c in range(self.columns_number)]))
        for c in range(self.columns_number):
            self._solver.add(self._solver.distinct([self._grid_z3[Position(r, c)] for r in range(self.rows_number)]))

    def _get_rows_number(self) -> int:
        all_positions = [pos for sublist, _, _ in self._regions_operators_results for pos in sublist]
        min_r = min(pos.r for pos in all_positions)
        max_r = max(pos.r for pos in all_positions)
        rows_number = max_r - min_r + 1
        return rows_number

    def _get_columns_number(self) -> int:
        all_positions = [pos for sublist, _, _ in self._regions_operators_results for pos in sublist]
        min_c = min(pos.c for pos in all_positions)
        max_c = max(pos.c for pos in all_positions)
        columns_numbers = max_c - min_c + 1
        return columns_numbers

    def _add_results_operations_constraints(self):
        for region, operator_str, result in self._regions_operators_results:
            if operator_str == '+':
                constraint = self._solver.sum([self._grid_z3[position] for position in region]) == result
            elif operator_str == 'x':
                constraint = reduce(operator.mul, [self._grid_z3[position] for position in region]) == result
            elif operator_str == '-':
                constraint = self._solver.Or(
                    reduce(operator.sub, [self._grid_z3[position] for position in region]) == result,
                    reduce(operator.sub, [self._grid_z3[position] for position in region]) == -result
                )
            elif operator_str == '/':
                constraint = self._solver.Or(
                    reduce(operator.truediv, [self._grid_z3[position] for position in region]) == result,
                    reduce(operator.truediv, [self._grid_z3[position] for position in reversed(region)]) == result
                )
            else:
                raise ValueError("Invalid operator_str")
            self._solver.add(constraint)
