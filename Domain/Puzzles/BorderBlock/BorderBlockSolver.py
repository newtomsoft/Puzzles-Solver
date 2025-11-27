from itertools import combinations

from z3 import Solver, Int, And, Not, Or, Distinct, ArithRef, sat

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class BorderBlockSolver(GameSolver):
    empty = None

    def __init__(self, grid: Grid, dots: list[Position]):
        self._input_grid = grid
        self._dots = dots
        self._rows_number = self._input_grid.rows_number
        self._columns_number = self._input_grid.columns_number
        self._max_region_id = max(value for position, value in self._input_grid if value is not None)
        self._grid_z3: Grid = Grid.empty()
        self._solver = Solver()
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Int(f"region_id_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()

        solution, _ = self._ensure_all_shapes_compliant()
        self._previous_solution = solution
        return solution

    def _ensure_all_shapes_compliant(self) -> tuple[Grid, int]:
        proposition_count = 0
        while self._solver.check() == sat:
            model = self._solver.model()
            proposition_count += 1
            proposition_grid = Grid(
                [[model.eval(self._grid_z3[Position(r, c)]).as_long() for c in range(self._columns_number)] for r in range(self._rows_number)])
            shapes = {circle_value: proposition_grid.get_all_shapes(circle_value) for circle_value in range(1, self._max_region_id + 1)}
            not_compliant_shapes = [(value, shapes_positions) for (value, shapes_positions) in shapes.items() if len(shapes_positions) > 1]
            if len(not_compliant_shapes) == 0:
                return proposition_grid, proposition_count

            self._solver.add(Not(And([self._grid_z3[position] == value for position, value in proposition_grid])))

            # for circle_value, shapes_positions in not_compliant_shapes:
            #     selected_circle_position = next(iter(self.circle_positions[circle_value].straddled_neighbors()))
            #     for shape_positions in shapes_positions:
            #         if selected_circle_position not in shape_positions:
            #             shape_constraints = [self._grid_z3[position] == circle_value for position in shape_positions]
            #             around_constraints = [self._grid_z3[position] == proposition_grid[position] for position in ShapeGenerator.around_shape(shape_positions) if position in proposition_grid]
            #             constraint = Not(And(shape_constraints + around_constraints))
            #             self._solver.add(constraint)

        return Grid.empty(), proposition_count

    def get_other_solution(self) -> Grid:
        self._solver.add(Not(And([self._grid_z3[position] == value for position, value in self._previous_solution])))
        solution, _ = self._ensure_all_shapes_compliant()
        self._previous_solution = solution
        return solution

    def _add_constraints(self):
        self._add_initials_constraints()
        self._add_dots_constraints()
        self._add_not_dots_constraints()

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

    def _add_edge_dot_constraints(self, neighbors_value: list[ArithRef]) -> bool:
        if len(neighbors_value) == 2:
            self._solver.add(neighbors_value[0] != neighbors_value[1])
            return True

        return False

    def _add_inside_dot_constraint(self, neighbors_value: list[ArithRef]):
        self._solver.add(Or([Distinct(trio) for trio in combinations(neighbors_value, 3)]))

    def _add_not_dots_constraints(self):
        self._add_not_edge_dot_constraints()
        self._add_not_inside_dot_constraints()

    def _add_not_edge_dot_constraints(self):
        empty_border_positions = self._get_empty_border_positions()
        for position in empty_border_positions:
            neighbors_value = [self._grid_z3[neighbor] for neighbor in position.straddled_neighbors() if neighbor in self._input_grid]
            self._solver.add(neighbors_value[0] == neighbors_value[1])

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

    def _add_not_inside_dot_constraints(self):
        inside_positions = self._get_inside_positions()
        for position in inside_positions:
            v1 = Int(f"v1{position}")
            v2 = Int(f"v2{position}")
            for neighbor_value in [self._grid_z3[neighbor] for neighbor in position.straddled_neighbors()]:
                self._solver.add(Or(neighbor_value == v1, neighbor_value == v2))

    def _get_inside_positions(self):
        first_position = Position(-0.5, -0.5)
        positions = set()
        for r in range(1, self._rows_number):
            for c in range(1, self._columns_number):
                positions.add(first_position + Position(r, c))

        positions -= set(self._dots)
        return positions
