from z3 import Solver, Not, And, Int, sat, Or, Implies

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Utils.ShapeGenerator import ShapeGenerator


class HakoiriSolver:
    def __init__(self, region_grid: Grid[int], value_grid: Grid[int]):
        self._region_grid = region_grid
        self._value_grid = value_grid
        self._rows_number = self._region_grid.rows_number
        self._columns_number = self._region_grid.columns_number
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Int(f"cell_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()
        return self._compute_solution()

    def _compute_solution(self) -> Grid:
        self._previous_solution, _ = self._ensure_all_filled_connected()
        return self._previous_solution

    def _ensure_all_filled_connected(self) -> tuple[Grid, int]:
        proposition_count = 0
        while self._solver.check() == sat:
            model = self._solver.model()
            proposition_count += 1
            current_grid = Grid([[(model.eval(self._grid_z3[Position(i, j)])).as_long() for j in range(self._columns_number)] for i in range(self._rows_number)])
            current_bool_grid = Grid([[(model.eval(self._grid_z3[Position(i, j)])).as_long() > 0 for j in range(self._columns_number)] for i in range(self._rows_number)])
            filled_shapes = current_bool_grid.get_all_shapes()
            if len(filled_shapes) == 1:
                return current_grid, proposition_count

            biggest_shape = max(filled_shapes, key=len)
            filled_shapes.remove(biggest_shape)
            for filled_shape in filled_shapes:
                shape_not_all_filled = Not(And([self._grid_z3[position] > 0 for position in filled_shape]))
                around_shape = ShapeGenerator.around_shape(filled_shape)
                around_not_all_empty = Not(And([self._grid_z3[position] == 0 for position in around_shape if position in self._grid_z3]))
                constraint = Or(shape_not_all_filled, around_not_all_empty)
                self._solver.add(constraint)

        return Grid.empty(), proposition_count

    def get_other_solution(self) -> Grid:
        self._solver.add(Not(And([self._grid_z3[position] == value for position, value in self._previous_solution if value > 0])))
        return self._compute_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_no_equal_neighbors_constraints()
        self._add_each_value_one_time_in_regions_constraints()

    def _add_initial_constraints(self):
        for position, value in self._value_grid:
            if value > 0:
                self._solver.add(self._grid_z3[position] == value)
            else:
                self._solver.add(self._grid_z3[position] >= 0, self._grid_z3[position] <= 3)

    def _add_no_equal_neighbors_constraints(self):
        for position, value in self._grid_z3:
            neighbors_positions = self._grid_z3.neighbors_positions(position, 'diagonal')
            for neighbor in neighbors_positions:
                self._solver.add(Implies(value > 0, self._grid_z3[neighbor] != value ))

    def _add_each_value_one_time_in_regions_constraints(self):
        positions_by_region = self._region_grid.get_regions()
        for region, positions in positions_by_region.items():
            for value in range(1, 4):
                self._solver.add(sum([self._grid_z3[position] == value for position in positions]) == 1)