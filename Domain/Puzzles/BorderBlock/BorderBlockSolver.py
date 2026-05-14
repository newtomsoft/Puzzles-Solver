from itertools import combinations
from typing import Collection

from z3 import Solver, Int, And, Not, Or, Distinct, Implies, If, Sum, sat, Bool

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class BorderBlockSolver(GameSolver):
    empty = None

    def __init__(self, grid: Grid, dots: Collection[Position]):
        self._input_grid = grid
        self._dots = dots
        self._rows_number = self._input_grid.rows_number
        self._columns_number = self._input_grid.columns_number
        self._max_region_id = max(value for position, value in self._input_grid if value is not None)
        self._grid_z3: Grid = Grid.empty()
        self._solver = Solver()
        self._previous_solution: Grid = Grid.empty()

    def _init_solver(self):
        self._grid_z3 = Grid([[Int(f"region_id_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._grid_z3.is_empty():
            self._init_solver()

        if self._solver.check() != sat:
            return Grid.empty()

        model = self._solver.model()
        solution = Grid(
            [[model.eval(self._grid_z3[Position(r, c)]).as_long() for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._previous_solution = solution
        return solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution.is_empty():
            return self.get_solution()

        self._solver.add(Not(And([self._grid_z3[position] == value for position, value in self._previous_solution])))
        return self.get_solution()

    def _add_constraints(self):
        self._add_initials_constraints()
        self._add_dots_constraints()
        self._add_not_dots_constraints()
        self._add_region_connectivity_constraints()

    def _add_region_connectivity_constraints(self):
        total_cells = self._rows_number * self._columns_number
        self._rank_vars = [[Int(f"rank_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)]
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                self._solver.add(self._rank_vars[r][c] >= 0)
                self._solver.add(self._rank_vars[r][c] < total_cells)

        for region_id in range(1, self._max_region_id + 1):
            root_vars = []
            region_cells = [Position(r, c) for r in range(self._rows_number) for c in range(self._columns_number)]

            for pos in region_cells:
                is_root = Bool(f"root_{region_id}_{pos.r}_{pos.c}")
                root_vars.append(is_root)
                in_region = (self._grid_z3[pos] == region_id)

                self._solver.add(Implies(is_root, in_region))
                self._solver.add(Implies(is_root, self._rank_vars[pos.r][pos.c] == 0))

                parent_conditions = []
                for neighbor in self._input_grid.neighbors_positions(pos):
                    neighbor_in_region = (self._grid_z3[neighbor] == region_id)
                    has_lower_rank = self._rank_vars[neighbor.r][neighbor.c] < self._rank_vars[pos.r][pos.c]
                    parent_conditions.append(And(neighbor_in_region, has_lower_rank))

                if parent_conditions:
                    self._solver.add(Implies(And(in_region, Not(is_root)), Or(*parent_conditions)))

            region_exists = Or([self._grid_z3[pos] == region_id for pos in region_cells])
            root_count = Sum([If(is_root, 1, 0) for is_root in root_vars])
            self._solver.add(Implies(region_exists, root_count == 1))

    def _add_initials_constraints(self):
        for position, value in self._input_grid:
            if value is None:
                self._solver.add(self._grid_z3[position] > 0, self._grid_z3[position] <= self._max_region_id)
            else:
                self._solver.add(self._grid_z3[position] == value)

    def _add_dots_constraints(self):
        for dot in self._dots:
            self._add_dot_constraint(dot)

    def _add_dot_constraint(self, dot: Position):
        neighbors_value = [self._grid_z3[position] for position in dot.straddled_neighbors() if position in self._input_grid]

        if self._add_edge_dot_constraints(neighbors_value):
            return

        self._add_inside_dot_constraint(neighbors_value)

    def _add_edge_dot_constraints(self, neighbors_value: list[Int]) -> bool:
        if len(neighbors_value) == 2:
            self._solver.add(neighbors_value[0] != neighbors_value[1])
            return True

        return False

    def _add_inside_dot_constraint(self, neighbors_value: list[Int]):
        self._solver.add(Or([Distinct(trio) for trio in combinations(neighbors_value, 3)]))

    def _add_not_dots_constraints(self):
        self._add_not_edge_dot_constraints()
        self._add_not_inside_dot_constraints()

    def _add_not_edge_dot_constraints(self):
        empty_border_positions = self._get_empty_border_positions()
        for position in empty_border_positions:
            neighbors_value = [self._grid_z3[neighbor] for neighbor in position.straddled_neighbors() if neighbor in self._input_grid]
            self._solver.add(neighbors_value[0] == neighbors_value[1])

    def _add_not_inside_dot_constraints(self):
        inside_positions = self._get_inside_positions()
        for position in inside_positions:
            v1 = Int(f"v1{position}")
            v2 = Int(f"v2{position}")
            for neighbor_value in [self._grid_z3[neighbor] for neighbor in position.straddled_neighbors()]:
                self._solver.add(Or(neighbor_value == v1, neighbor_value == v2))

    def _get_empty_border_positions(self) -> set[Position]:
        first_position = Position(-0.5, -0.5)
        positions = set()
        for c in range(1, self._columns_number):
            positions.add(first_position + Position(0, c))
            positions.add(first_position + Position(self._rows_number, c))

        for r in range(1, self._rows_number):
            positions.add(first_position + Position(r, 0))
            positions.add(first_position + Position(r, self._columns_number))

        positions -= set(self._dots)
        return positions

    def _get_inside_positions(self):
        first_position = Position(-0.5, -0.5)
        positions = set()
        for r in range(1, self._rows_number):
            for c in range(1, self._columns_number):
                positions.add(first_position + Position(r, c))

        positions -= set(self._dots)
        return positions
