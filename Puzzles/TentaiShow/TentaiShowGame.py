from typing import Tuple, Dict

from z3 import Int, Solver, sat, Not, And, Implies, Or

from Utils.Grid import Grid
from Utils.Position import Position
from Utils.ShapeGenerator import ShapeGenerator


class TentaiShowGame:
    def __init__(self, grid_size: Tuple[int, int], circles_positions: Dict[int, Position]):
        self._grid = Grid([[0 for _ in range(grid_size[1])] for _ in range(grid_size[0])])
        self.circle_positions = circles_positions
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._solver = None
        self._grid_z3 = None
        self._last_solution = None

    def _init_solver(self):
        self._grid_z3 = Grid([[Int(f"grid{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._solver = Solver()
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._solver is None:
            self._init_solver()

        solution, _ = self._ensure_all_shapes_compliant()
        self._last_solution = solution
        return solution

    def _ensure_all_shapes_compliant(self) -> (Grid, int):
        proposition_count = 0
        while self._solver.check() == sat:
            model = self._solver.model()
            proposition_count += 1
            grid = Grid([[model.eval(self._grid_z3[Position(r, c)]).as_long() for c in range(self.columns_number)] for r in range(self.rows_number)])

            is_solution = True
            for circle_value in self.circle_positions.keys():
                if not grid.are_all_cells_connected(circle_value):
                    is_solution = False
                    break
            if is_solution:
                return grid, proposition_count

            circle_shapes = {circle_value: grid.get_all_shapes(circle_value) for circle_value in self.circle_positions.keys()}
            for circle_value, shapes in circle_shapes.items():
                if len(shapes) == 1:
                    continue
                circle_positions = self.circle_positions[circle_value].straddled_neighbors()
                for positions in shapes:
                    if next(iter(circle_positions)) not in positions:
                        shape_constraints = [self._grid_z3[position] == circle_value for position in positions]
                        around_constraints = [self._grid_z3[position] == grid[position] for position in ShapeGenerator.around_shape(positions) if position in grid]
                        constraint = Not(And(shape_constraints + around_constraints))
                        self._solver.add(constraint)

        return Grid.empty(), proposition_count

    def get_other_solution(self):
        self._exclude_previous_solution()
        return self.get_solution()

    def _exclude_previous_solution(self):
        previous_solution_constraints = []
        for position, value in self._last_solution:
            previous_solution_constraints.append(self._grid_z3[position] == value)
        self._solver.add(Not(And(previous_solution_constraints)))

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_symmetry_constraints()
        self._add_neighbors_constraints()

    def _add_initial_constraints(self):
        self._add_range_constraints()
        self._add_circles_initial_constraints()

    def _add_range_constraints(self):
        self._solver.add([self._grid_z3[position] >= min(self.circle_positions.keys()) for position, _ in self._grid])
        self._solver.add([self._grid_z3[position] <= max(self.circle_positions.keys()) for position, _ in self._grid])

    def _add_circles_initial_constraints(self):
        for circle_value, current_position in self.circle_positions.items():
            if int(current_position.r) == current_position.r and int(current_position.c) == current_position.c:
                current_position = Position(int(current_position.r), int(current_position.c))
                self._solver.add(self._grid_z3[current_position] == circle_value)
                self._grid.set_value(current_position, circle_value)
                continue
            positions = self._grid.straddled_neighbors_positions(current_position)
            for position in positions:
                self._solver.add(self._grid_z3[position] == circle_value)
                self._grid.set_value(position, circle_value)

    def _add_symmetry_constraints(self):
        for position, value in self._grid:
            if value != 0:
                continue
            for circle_value, circle_position in self.circle_positions.items():
                symmetric_position = position.symmetric(circle_position)
                if symmetric_position in self._grid:
                    self._solver.add(Implies(self._grid_z3[position] == circle_value, self._grid_z3[symmetric_position] == circle_value))
                    self._solver.add(Implies(self._grid_z3[position] != circle_value, self._grid_z3[symmetric_position] != circle_value))
                else:
                    self._solver.add(self._grid_z3[position] != circle_value)

    def _add_neighbors_constraints(self):
        for position, value in self._grid:
            if value == 0:
                neighbors = self._grid.neighbors_positions(position)
                self._solver.add(Or([self._grid_z3[position] == self._grid_z3[neighbor] for neighbor in neighbors]))
