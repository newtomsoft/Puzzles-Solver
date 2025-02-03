from typing import Tuple, Dict

from Ports.SolverEngine import SolverEngine
from Puzzles.GameSolver import GameSolver
from Utils.Grid import Grid
from Utils.Position import Position
from Utils.ShapeGenerator import ShapeGenerator


class TentaiShowSolver(GameSolver):
    def __init__(self, grid_size: Tuple[int, int], circles_positions: Dict[int, Position], solver_engine: SolverEngine):
        self._grid = Grid([[0 for _ in range(grid_size[1])] for _ in range(grid_size[0])])
        self.circle_positions = circles_positions
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._solver = solver_engine
        self._grid_z3 = None
        self._last_solution = None

    def _init_solver(self):
        self._grid_z3 = Grid([[self._solver.int(f"grid{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.has_constraints():
            self._init_solver()

        solution, _ = self._ensure_all_shapes_compliant()
        self._last_solution = solution
        return solution

    def _ensure_all_shapes_compliant(self) -> (Grid, int):
        proposition_count = 0
        while self._solver.has_solution() == sat:
            model = self._solver.model()
            proposition_count += 1
            if proposition_count % 10 == 0:
                print('.', end='', flush=True)
            grid = Grid([[model.eval(self._grid_z3[Position(r, c)]).as_long() for c in range(self.columns_number)] for r in range(self.rows_number)])

            circle_shapes = {circle_value: grid.get_all_shapes(circle_value) for circle_value in self.circle_positions.keys()}
            not_compliant_shapes = [(circle_value, shapes_positions) for (circle_value, shapes_positions) in circle_shapes.items() if len(shapes_positions) > 1]
            if len(not_compliant_shapes) == 0:
                return grid, proposition_count

            for circle_value, shapes_positions in not_compliant_shapes:
                selected_circle_position = next(iter(self.circle_positions[circle_value].straddled_neighbors()))
                for shape_positions in shapes_positions:
                    if selected_circle_position not in shape_positions:
                        shape_constraints = [self._grid_z3[position] == circle_value for position in shape_positions]
                        around_constraints = [self._grid_z3[position] == grid[position] for position in ShapeGenerator.around_shape(shape_positions) if position in grid]
                        constraint = self._solver.Not(self._solver.And(shape_constraints + around_constraints))
                        self._solver.add(constraint)

        return Grid.empty(), proposition_count

    def get_other_solution(self):
        self._exclude_previous_solution()
        return self.get_solution()

    def _exclude_previous_solution(self):
        previous_solution_constraints = []
        for position, value in self._last_solution:
            previous_solution_constraints.append(self._grid_z3[position] == value)
        self._solver.add(self._solver.Not(self._solver.And(previous_solution_constraints)))

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
                    self._solver.add(self._solver.Implies(self._grid_z3[position] == circle_value, self._grid_z3[symmetric_position] == circle_value))
                    self._solver.add(self._solver.Implies(self._grid_z3[position] != circle_value, self._grid_z3[symmetric_position] != circle_value))
                else:
                    self._solver.add(self._grid_z3[position] != circle_value)

    def _add_neighbors_constraints(self):
        for position, value in self._grid:
            if value == 0:
                neighbors = self._grid.neighbors_positions(position)
                self._solver.add(self._solver.Or([self._grid_z3[position] == self._grid_z3[neighbor] for neighbor in neighbors]))
