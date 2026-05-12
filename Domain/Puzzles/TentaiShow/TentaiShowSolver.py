from typing import Tuple, Dict

from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


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
        min_value = min(self.circle_positions.keys())
        max_value = max(self.circle_positions.keys())
        self._grid_vars = Grid([[self._model.new_int_var(min_value, max_value, f"grid{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._grid_vars is None:
            self._init_solver()

        status = self._solver.solve(self._model)
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            solution = Grid([[self._solver.value(self._grid_vars[Position(r, c)]) for c in range(self.columns_number)] for r in range(self.rows_number)])
            self._previous_solution = solution
            return solution

        return Grid.empty()

    def get_other_solution(self):
        self._exclude_previous_solution()
        return self.get_solution()

    def _exclude_previous_solution(self):
        previous_solution_literals = []
        for position, value in self._previous_solution:
            temp_var = self._model.new_bool_var(f"prev_{position.r}_{position.c}")
            self._model.add(self._grid_vars[position] == value).only_enforce_if(temp_var)
            self._model.add(self._grid_vars[position] != value).only_enforce_if(temp_var.Not())
            previous_solution_literals.append(temp_var)

        if previous_solution_literals:
            self._model.add_bool_or([lit.Not() for lit in previous_solution_literals])

    def _add_constraints(self):
        self._add_circles_initial_constraints()
        self._add_symmetry_constraints()
        self._add_neighbors_constraints()
        self._add_region_connectivity_constraints()

    def _add_circles_initial_constraints(self):
        for circle_value, current_position in self.circle_positions.items():
            if int(current_position.r) == current_position.r and int(current_position.c) == current_position.c:
                current_position = Position(int(current_position.r), int(current_position.c))
                self._model.add(self._grid_vars[current_position] == circle_value)
                self._grid.set_value(current_position, circle_value)
                continue
            positions = self._grid.straddled_neighbors_positions(current_position)
            for position in positions:
                self._model.add(self._grid_vars[position] == circle_value)
                self._grid.set_value(position, circle_value)

    def _add_symmetry_constraints(self):
        for position, value in self._grid:
            if value != 0:
                continue
            for circle_value, circle_position in self.circle_positions.items():
                symmetric_position = position.symmetric(circle_position)
                if symmetric_position in self._grid:
                    both_v = self._model.new_bool_var(f"both_{position.r}_{position.c}_{circle_value}")
                    self._model.add(self._grid_vars[position] == circle_value).only_enforce_if(both_v)
                    self._model.add(self._grid_vars[position] != circle_value).only_enforce_if(both_v.Not())
                    self._model.add(self._grid_vars[symmetric_position] == circle_value).only_enforce_if(both_v)
                    self._model.add(self._grid_vars[symmetric_position] != circle_value).only_enforce_if(both_v.Not())
                else:
                    self._model.add(self._grid_vars[position] != circle_value)

    def _add_neighbors_constraints(self):
        for position, value in self._grid:
            if value == 0:
                neighbors = self._grid.neighbors_positions(position)
                if neighbors:
                    same_value_neighbors = []
                    for neighbor in neighbors:
                        same_value = self._model.new_bool_var(f"same_value_{position.r}_{position.c}_{neighbor.r}_{neighbor.c}")
                        self._model.add(self._grid_vars[position] == self._grid_vars[neighbor]).only_enforce_if(same_value)
                        self._model.add(self._grid_vars[position] != self._grid_vars[neighbor]).only_enforce_if(same_value.Not())
                        same_value_neighbors.append(same_value)

                    if same_value_neighbors:
                        self._model.add_bool_or(same_value_neighbors)

    def _add_region_connectivity_constraints(self):
        max_dist = self.rows_number * self.columns_number
        for circle_value, circle_position in self.circle_positions.items():
            if int(circle_position.r) == circle_position.r and int(circle_position.c) == circle_position.c:
                root = Position(int(circle_position.r), int(circle_position.c))
            else:
                positions = list(self._grid.straddled_neighbors_positions(circle_position))
                root = positions[0]

            depth = {}
            for r in range(self.rows_number):
                for c in range(self.columns_number):
                    depth[(r, c)] = self._model.new_int_var(0, max_dist, f"depth_{circle_value}_{r}_{c}")

            self._model.add(depth[(root.r, root.c)] == 0)

            for r in range(self.rows_number):
                for c in range(self.columns_number):
                    pos = Position(r, c)
                    if pos == root:
                        continue

                    fixed_value = self._grid[pos]
                    if fixed_value == circle_value:
                        self._model.add(depth[(r, c)] > 0)
                        neighbors = self._grid.neighbors_positions(pos)
                        parent_vars = []
                        for neighbor in neighbors:
                            neighbor_fixed = self._grid[neighbor]
                            if neighbor_fixed != 0 and neighbor_fixed != circle_value:
                                continue
                            p_ok = self._model.new_bool_var(f"parent_{circle_value}_{r}_{c}_{neighbor.r}_{neighbor.c}")
                            self._model.add(self._grid_vars[neighbor] == circle_value).only_enforce_if(p_ok)
                            self._model.add(depth[(r, c)] == depth[(neighbor.r, neighbor.c)] + 1).only_enforce_if(p_ok)
                            parent_vars.append(p_ok)
                        if parent_vars:
                            self._model.add_bool_or(parent_vars)
                    elif fixed_value != 0:
                        self._model.add(depth[(r, c)] == 0)
                    else:
                        is_v = self._model.new_bool_var(f"is_{circle_value}_{r}_{c}")
                        self._model.add(self._grid_vars[pos] == circle_value).only_enforce_if(is_v)
                        self._model.add(self._grid_vars[pos] != circle_value).only_enforce_if(is_v.Not())

                        self._model.add(depth[(r, c)] == 0).only_enforce_if(is_v.Not())
                        self._model.add(depth[(r, c)] > 0).only_enforce_if(is_v)

                        neighbors = self._grid.neighbors_positions(pos)
                        parent_vars = []
                        for neighbor in neighbors:
                            neighbor_fixed = self._grid[neighbor]
                            if neighbor_fixed != 0 and neighbor_fixed != circle_value:
                                continue
                            p_ok = self._model.new_bool_var(f"parent_{circle_value}_{r}_{c}_{neighbor.r}_{neighbor.c}")
                            self._model.add(self._grid_vars[neighbor] == circle_value).only_enforce_if(p_ok)
                            self._model.add(depth[(r, c)] == depth[(neighbor.r, neighbor.c)] + 1).only_enforce_if(p_ok)
                            parent_vars.append(p_ok)

                        if parent_vars:
                            self._model.add_bool_or(parent_vars).only_enforce_if(is_v)
