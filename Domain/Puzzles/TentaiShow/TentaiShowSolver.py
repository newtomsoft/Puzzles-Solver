from typing import Tuple, Dict

from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator


class TentaiShowSolver(GameSolver):
    def __init__(self, grid_size: Tuple[int, int], circles_positions: Dict[int, Position]):
        self._grid = Grid([[0 for _ in range(grid_size[1])] for _ in range(grid_size[0])])
        self.circle_positions = circles_positions
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars = None
        self._previous_solution = None

    def _init_solver(self):
        # Determine the range of values for the grid cells
        min_value = min(self.circle_positions.keys())
        max_value = max(self.circle_positions.keys())
        self._grid_vars = Grid([[self._model.NewIntVar(min_value, max_value, f"grid{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._grid_vars is None:
            self._init_solver()

        solution, _ = self._ensure_all_shapes_compliant()
        self._previous_solution = solution
        return solution

    def _ensure_all_shapes_compliant(self) -> (Grid, int):
        proposition_count = 0
        status = self._solver.Solve(self._model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            proposition_count += 1

            grid = Grid([[self._solver.Value(self._grid_vars[Position(r, c)]) for c in range(self.columns_number)] for r in range(self.rows_number)])

            circle_shapes = {circle_value: grid.get_all_shapes(circle_value) for circle_value in self.circle_positions.keys()}
            not_compliant_shapes = [(circle_value, shapes_positions) for (circle_value, shapes_positions) in circle_shapes.items() if len(shapes_positions) > 1]

            while len(not_compliant_shapes) > 0:
                for circle_value, shapes_positions in not_compliant_shapes:
                    selected_circle_position = next(iter(self.circle_positions[circle_value].straddled_neighbors()))
                    for shape_positions in shapes_positions:
                        if selected_circle_position not in shape_positions:
                            shape_literals = []
                            for position in shape_positions:
                                temp_var = self._model.NewBoolVar(f"shape_{circle_value}_{position.r}_{position.c}")
                                self._model.Add(self._grid_vars[position] == circle_value).OnlyEnforceIf(temp_var)
                                self._model.Add(self._grid_vars[position] != circle_value).OnlyEnforceIf(temp_var.Not())
                                shape_literals.append(temp_var)

                            around_literals = []
                            for position in ShapeGenerator.around_shape(shape_positions):
                                if position in grid:
                                    temp_var = self._model.NewBoolVar(f"around_{circle_value}_{position.r}_{position.c}")
                                    self._model.Add(self._grid_vars[position] == grid[position]).OnlyEnforceIf(temp_var)
                                    self._model.Add(self._grid_vars[position] != grid[position]).OnlyEnforceIf(temp_var.Not())
                                    around_literals.append(temp_var)

                            if shape_literals and around_literals:
                                all_shape = self._model.NewBoolVar(f"all_shape_{circle_value}")
                                self._model.AddBoolAnd(shape_literals).OnlyEnforceIf(all_shape)
                                self._model.AddBoolOr([lit.Not() for lit in shape_literals]).OnlyEnforceIf(all_shape.Not())

                                all_around = self._model.NewBoolVar(f"all_around_{circle_value}")
                                self._model.AddBoolAnd(around_literals).OnlyEnforceIf(all_around)
                                self._model.AddBoolOr([lit.Not() for lit in around_literals]).OnlyEnforceIf(all_around.Not())

                                self._model.AddBoolOr([all_shape.Not(), all_around.Not()])

                status = self._solver.Solve(self._model)
                if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
                    break

                proposition_count += 1

                grid = Grid([[self._solver.Value(self._grid_vars[Position(r, c)]) for c in range(self.columns_number)] for r in range(self.rows_number)])

                circle_shapes = {circle_value: grid.get_all_shapes(circle_value) for circle_value in self.circle_positions.keys()}
                not_compliant_shapes = [(circle_value, shapes_positions) for (circle_value, shapes_positions) in circle_shapes.items() if len(shapes_positions) > 1]

            if len(not_compliant_shapes) == 0:
                return grid, proposition_count

        return Grid.empty(), proposition_count

    def get_other_solution(self):
        self._exclude_previous_solution()
        return self.get_solution()

    def _exclude_previous_solution(self):
        previous_solution_literals = []
        for position, value in self._previous_solution:
            temp_var = self._model.NewBoolVar(f"prev_{position.r}_{position.c}")
            self._model.Add(self._grid_vars[position] == value).OnlyEnforceIf(temp_var)
            self._model.Add(self._grid_vars[position] != value).OnlyEnforceIf(temp_var.Not())
            previous_solution_literals.append(temp_var)

        if previous_solution_literals:
            self._model.AddBoolOr([lit.Not() for lit in previous_solution_literals])

    def _add_constraints(self):
        self._add_circles_initial_constraints()
        self._add_symmetry_constraints()
        self._add_neighbors_constraints()

    def _add_circles_initial_constraints(self):
        for circle_value, current_position in self.circle_positions.items():
            if int(current_position.r) == current_position.r and int(current_position.c) == current_position.c:
                current_position = Position(int(current_position.r), int(current_position.c))
                self._model.Add(self._grid_vars[current_position] == circle_value)
                self._grid.set_value(current_position, circle_value)
                continue
            positions = self._grid.straddled_neighbors_positions(current_position)
            for position in positions:
                self._model.Add(self._grid_vars[position] == circle_value)
                self._grid.set_value(position, circle_value)

    def _add_symmetry_constraints(self):
        for position, value in self._grid:
            if value != 0:
                continue
            for circle_value, circle_position in self.circle_positions.items():
                symmetric_position = position.symmetric(circle_position)
                if symmetric_position in self._grid:
                    pos_equals_circle = self._model.NewBoolVar(f"pos_equals_circle_{position.r}_{position.c}_{circle_value}")
                    sym_equals_circle = self._model.NewBoolVar(f"sym_equals_circle_{symmetric_position.r}_{symmetric_position.c}_{circle_value}")

                    self._model.Add(self._grid_vars[position] == circle_value).OnlyEnforceIf(pos_equals_circle)
                    self._model.Add(self._grid_vars[position] != circle_value).OnlyEnforceIf(pos_equals_circle.Not())
                    self._model.Add(self._grid_vars[symmetric_position] == circle_value).OnlyEnforceIf(sym_equals_circle)
                    self._model.Add(self._grid_vars[symmetric_position] != circle_value).OnlyEnforceIf(sym_equals_circle.Not())

                    self._model.AddImplication(pos_equals_circle, sym_equals_circle)
                    self._model.AddImplication(pos_equals_circle.Not(), sym_equals_circle.Not())
                else:
                    self._model.Add(self._grid_vars[position] != circle_value)

    def _add_neighbors_constraints(self):
        for position, value in self._grid:
            if value == 0:
                neighbors = self._grid.neighbors_positions(position)
                if neighbors:
                    same_value_neighbors = []
                    for neighbor in neighbors:
                        same_value = self._model.NewBoolVar(f"same_value_{position.r}_{position.c}_{neighbor.r}_{neighbor.c}")
                        self._model.Add(self._grid_vars[position] == self._grid_vars[neighbor]).OnlyEnforceIf(same_value)
                        self._model.Add(self._grid_vars[position] != self._grid_vars[neighbor]).OnlyEnforceIf(same_value.Not())
                        same_value_neighbors.append(same_value)

                    if same_value_neighbors:
                        self._model.AddBoolOr(same_value_neighbors)
