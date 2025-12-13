from collections import defaultdict

from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class RenkatsuSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars = None
        self._previous_solution: Grid | None = None
        self._compute_numbers_occurs_in_regions()
        self._regions_count = self._numbers_count[1]
        self._compute_regions_length()

    def _compute_numbers_occurs_in_regions(self):
        self._numbers_count = defaultdict(int)
        for _, value in self._grid:
            self._numbers_count[value] += 1

    def _compute_regions_length(self):
        self._region_size_by_id = defaultdict(int)
        region_count = 0
        current_region_id = 1
        for number, number_count in sorted(self._numbers_count.items(), reverse=True):
            remaining_region_count = number_count - region_count
            if remaining_region_count == 0:
                continue
            region_count += remaining_region_count
            for i in range(current_region_id, current_region_id + remaining_region_count):
                self._region_size_by_id[i] = number
            current_region_id += remaining_region_count

    def get_solution(self) -> Grid:
        self._grid_vars = {}
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                self._grid_vars[(r, c)] = self._model.NewIntVar(1, self._regions_count, f"grid_{r}_{c}")

        self._add_constraints()
        return self._compute_solution()

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return Grid.empty()

        constraints = []
        for region_id in range(1, self._regions_count + 1):
            current_region_positions = [position for position, value in self._previous_solution if value == region_id]
            if not current_region_positions:
                continue

            same_value_literals = []
            for i in range(1, len(current_region_positions)):
                pos0 = current_region_positions[0]
                posi = current_region_positions[i]
                same_value_literals.append(
                    self._model.NewBoolVar(f"same_value_{region_id}_{i}")
                )
                self._model.Add(
                    self._grid_vars[(pos0.r, pos0.c)] == self._grid_vars[(posi.r, posi.c)]
                ).OnlyEnforceIf(same_value_literals[-1])
                self._model.Add(
                    self._grid_vars[(pos0.r, pos0.c)] != self._grid_vars[(posi.r, posi.c)]
                ).OnlyEnforceIf(same_value_literals[-1].Not())

            if same_value_literals:
                not_all_same = self._model.NewBoolVar(f"not_all_same_{region_id}")
                self._model.AddBoolAnd(same_value_literals).OnlyEnforceIf(not_all_same.Not())
                self._model.AddBoolOr([lit.Not() for lit in same_value_literals]).OnlyEnforceIf(not_all_same)
                constraints.append(not_all_same)

        if constraints:
            self._model.AddBoolOr(constraints)

        return self._compute_solution()

    def _compute_solution(self) -> Grid:
        status = self._solver.Solve(self._model)
        if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
            return Grid.empty()

        non_ordered_solution = Grid([[self._solver.Value(self._grid_vars[(i, j)]) for j in range(self.columns_number)] for i in range(self.rows_number)])
        solution = self._order_values_by_position(non_ordered_solution)
        self._previous_solution = solution
        return solution

    def _add_constraints(self):
        self._add_same_numbers_in_distincts_regions_constraints()
        self._add_regions_size_constraints()
        self._add_connected_cells_regions_constraints()

    def _add_same_numbers_in_distincts_regions_constraints(self):
        for number in self._numbers_count.keys():
            positions = [position for position, value in self._grid if value == number]
            if len(positions) > 1:
                for i in range(len(positions)):
                    for j in range(i + 1, len(positions)):
                        pos_i = positions[i]
                        pos_j = positions[j]
                        self._model.Add(self._grid_vars[(pos_i.r, pos_i.c)] != self._grid_vars[(pos_j.r, pos_j.c)])

    def _add_regions_size_constraints(self):
        for region_id, region_size in self._region_size_by_id.items():
            region_cells = []
            for r in range(self.rows_number):
                for c in range(self.columns_number):
                    is_in_region = self._model.NewBoolVar(f"is_in_region_{region_id}_{r}_{c}")
                    self._model.Add(self._grid_vars[(r, c)] == region_id).OnlyEnforceIf(is_in_region)
                    self._model.Add(self._grid_vars[(r, c)] != region_id).OnlyEnforceIf(is_in_region.Not())
                    region_cells.append(is_in_region)

            self._model.Add(sum(region_cells) == region_size)

    def _add_connected_cells_regions_constraints(self):
        for region_id in range(1, self._regions_count + 1):
            self._add_connected_cells_region_constraints(region_id)

    def _add_connected_cells_region_constraints(self, region_id: int):
        step_vars = {}
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                max_step = self.rows_number * self.columns_number
                step_vars[(r, c)] = self._model.NewIntVar(0, max_step, f"step_{region_id}_{r}_{c}")

                is_in_region = self._model.NewBoolVar(f"is_in_region_{region_id}_{r}_{c}")
                self._model.Add(self._grid_vars[(r, c)] == region_id).OnlyEnforceIf(is_in_region)
                self._model.Add(self._grid_vars[(r, c)] != region_id).OnlyEnforceIf(is_in_region.Not())

                self._model.Add(step_vars[(r, c)] >= 1).OnlyEnforceIf(is_in_region)
                self._model.Add(step_vars[(r, c)] == 0).OnlyEnforceIf(is_in_region.Not())

        root_cells = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                is_root = self._model.NewBoolVar(f"is_root_{region_id}_{r}_{c}")
                self._model.Add(step_vars[(r, c)] == 1).OnlyEnforceIf(is_root)
                self._model.Add(step_vars[(r, c)] != 1).OnlyEnforceIf(is_root.Not())
                root_cells.append(is_root)

        self._model.AddExactlyOne(root_cells)

        for r in range(self.rows_number):
            for c in range(self.columns_number):
                is_non_root_in_region = self._model.NewBoolVar(f"is_non_root_{region_id}_{r}_{c}")
                self._model.Add(step_vars[(r, c)] > 1).OnlyEnforceIf(is_non_root_in_region)
                self._model.Add(step_vars[(r, c)] <= 1).OnlyEnforceIf(is_non_root_in_region.Not())

                adjacent_constraints = []

                if r > 0:
                    is_connected_up = self._model.NewBoolVar(f"is_connected_up_{region_id}_{r}_{c}")
                    self._model.Add(self._grid_vars[(r - 1, c)] == region_id).OnlyEnforceIf(is_connected_up)
                    self._model.Add(step_vars[(r - 1, c)] == step_vars[(r, c)] - 1).OnlyEnforceIf(is_connected_up)
                    adjacent_constraints.append(is_connected_up)

                if r < self.rows_number - 1:
                    is_connected_down = self._model.NewBoolVar(f"is_connected_down_{region_id}_{r}_{c}")
                    self._model.Add(self._grid_vars[(r + 1, c)] == region_id).OnlyEnforceIf(is_connected_down)
                    self._model.Add(step_vars[(r + 1, c)] == step_vars[(r, c)] - 1).OnlyEnforceIf(is_connected_down)
                    adjacent_constraints.append(is_connected_down)

                if c > 0:
                    is_connected_left = self._model.NewBoolVar(f"is_connected_left_{region_id}_{r}_{c}")
                    self._model.Add(self._grid_vars[(r, c - 1)] == region_id).OnlyEnforceIf(is_connected_left)
                    self._model.Add(step_vars[(r, c - 1)] == step_vars[(r, c)] - 1).OnlyEnforceIf(is_connected_left)
                    adjacent_constraints.append(is_connected_left)

                if c < self.columns_number - 1:
                    is_connected_right = self._model.NewBoolVar(f"is_connected_right_{region_id}_{r}_{c}")
                    self._model.Add(self._grid_vars[(r, c + 1)] == region_id).OnlyEnforceIf(is_connected_right)
                    self._model.Add(step_vars[(r, c + 1)] == step_vars[(r, c)] - 1).OnlyEnforceIf(is_connected_right)
                    adjacent_constraints.append(is_connected_right)

                if adjacent_constraints:
                    self._model.AddBoolOr(adjacent_constraints).OnlyEnforceIf(is_non_root_in_region)

    def _order_values_by_position(self, old_grid: Grid) -> Grid:
        new_value_by_old_value = {}
        current_value = 1
        new_grid = Grid([[0 for _ in range(self.columns_number)] for _ in range(self.rows_number)])
        for position, old_value in old_grid:
            if not (new_value := new_value_by_old_value.get(old_value)):
                new_value_by_old_value[old_value] = current_value
                new_value = current_value
                current_value += 1
            new_grid[position] = new_value

        return new_grid
