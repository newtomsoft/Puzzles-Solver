import math
import re
from collections import defaultdict

from z3 import Solver, Not, And, unsat, Or, Int, Distinct, Abs

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class KenKenSolver(GameSolver):
    def __init__(self, regions_grid: Grid, operations_grid: Grid):
        self.rows_number = regions_grid.rows_number
        self.columns_number = regions_grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("KenKen grid must be square")
        if operations_grid.rows_number != self.rows_number or operations_grid.columns_number != self.columns_number:
            raise ValueError("Regions grid and operations grid must have the same dimensions")

        self._regions_operators_results = self._parse_grids(regions_grid, operations_grid)
        self._grid_z3 = None
        self._solver = Solver()
        self._previous_solution: Grid | None = None

    def _parse_grids(self, regions_grid: Grid, operations_grid: Grid) -> list[tuple[list[Position], str, int]]:
        regions_map = defaultdict(list)
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                region_id = regions_grid[r][c]
                regions_map[region_id].append(Position(r, c))

        results = []
        for positions in regions_map.values():
            top_left = sorted(positions, key=lambda p: (p.r, p.c))[0]
            op_value = operations_grid[top_left]

            if op_value is None:
                # If no operation is present at the top-left, we assume it's just a number
                # which implies a sum constraint (or equality for single cell)
                # However, usually we expect a value. If it's completely missing, that's an issue.
                # But let's look at the regex handling.
                pass

            s_val = str(op_value).strip()
            if not s_val:
                 raise ValueError(f"No operation defined for region at {top_left}")

            # Match number then optional operator
            match = re.match(r"^(\d+)([+\-x÷]?)$", s_val)
            if not match:
                raise ValueError(f"Invalid operation format '{s_val}' at {top_left}")

            result_num = int(match.group(1))
            operator = match.group(2)

            if not operator:
                operator = '+'

            results.append((positions, operator, result_num))

        return results

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
