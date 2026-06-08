from typing import Collection

from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class NanroSolver(GameSolver):
    no_filled_value = 0

    def __init__(self, values_grid: Grid, regions_grid: Grid):
        super().__init__()
        self._values_grid = values_grid
        self._regions_positions_by_id = regions_grid.get_regions()
        self.rows_number = self._values_grid.rows_number
        self.columns_number = self._values_grid.columns_number
        self._grid_z3: Grid | None = None
        self._model = cp_model.CpModel()
        self._previous_solution: Grid | None = None
        self._solver_initialized = False
        self._exclude_counter = 0

    def _init_solver(self):
        max_region_size = max(len(p) for p in self._regions_positions_by_id.values())
        self._grid_z3 = Grid([[self._model.new_int_var(0, max_region_size, f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver_initialized:
            self._solver_initialized = True
            self._init_solver()

        solution, _ = self._ensure_all_values_cells_connected()
        self._previous_solution = solution
        return solution

    def get_other_solution(self):
        lits = []
        for position, value in [(position, value) for (position, value) in self._previous_solution if value > self.no_filled_value]:
            b = self._model.new_bool_var(f"block_{position.r}_{position.c}")
            self._model.Add(self._grid_z3[position] == value).OnlyEnforceIf(b)
            self._model.Add(self._grid_z3[position] != value).OnlyEnforceIf(b.Not())
            lits.append(b)
        self._model.Add(sum(lits) <= len(lits) - 1)

        return self.get_solution()

    def _ensure_all_values_cells_connected(self):
        proposition_count = 0
        while self._solver.Solve(self._model) in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            proposition_count += 1
            grid_bool = Grid([[self._solver.Value(self._grid_z3.value(i, j)) != self.no_filled_value for j in range(self.columns_number)] for i in range(self.rows_number)])
            connected_values = grid_bool.get_all_shapes(value=True)
            if len(connected_values) == 1:
                solution = Grid([[self._solver.Value(self._grid_z3.value(i, j)) for j in range(self.columns_number)] for i in range(self.rows_number)])
                return solution, proposition_count

            wrong_solution = Grid([[self._solver.Value(self._grid_z3.value(i, j)) for j in range(self.columns_number)] for i in range(self.rows_number)])
            lits = []
            for position, value in wrong_solution:
                self._exclude_counter += 1
                b = self._model.new_bool_var(f"exclude_{self._exclude_counter}_{position.r}_{position.c}")
                self._model.Add(self._grid_z3[position] == value).OnlyEnforceIf(b)
                self._model.Add(self._grid_z3[position] != value).OnlyEnforceIf(b.Not())
                lits.append(b)
            self._model.Add(sum(lits) <= len(lits) - 1)

        return Grid.empty(), proposition_count

    def _add_constraints(self):
        self._add_initial_values_constraints()
        self._add_no_square_values_constraints()
        self._add_no_adjacents_same_values_with_other_regions__constraints()
        self._add_values_by_region_constraints()
        self._add_no_isolated_values_constraints()

    def _add_initial_values_constraints(self):
        for position, value in [(position, value) for (position, value) in self._values_grid if value != self.no_filled_value]:
            self._model.Add(self._grid_z3[position] == value)

    def _add_no_square_values_constraints(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                filled_vars = []
                for dr, dc in [(0, 0), (1, 0), (0, 1), (1, 1)]:
                    b = self._model.new_bool_var(f"filled_{r}_{c}_{dr}_{dc}")
                    self._model.Add(self._grid_z3[r + dr][c + dc] != self.no_filled_value).OnlyEnforceIf(b)
                    self._model.Add(self._grid_z3[r + dr][c + dc] == self.no_filled_value).OnlyEnforceIf(b.Not())
                    filled_vars.append(b)
                self._model.AddBoolOr([v.Not() for v in filled_vars])

    def _add_values_by_region_constraints(self):
        for region_positions in self._regions_positions_by_id.values():
            self._add_same_values_or_empty_constraints(list(region_positions))
            self._add_count_values(region_positions)

    def _add_same_values_or_empty_constraints(self, positions: list[Position]):
        value = max([self._values_grid[position] for position in positions])
        if value != self.no_filled_value:
            for position in positions:
                b_val = self._model.new_bool_var(f"val_{position.r}_{position.c}")
                self._model.Add(self._grid_z3[position] == value).OnlyEnforceIf(b_val)
                self._model.Add(self._grid_z3[position] == self.no_filled_value).OnlyEnforceIf(b_val.Not())
        else:
            region_list = list(positions)
            for index, position in enumerate(region_list[:-2]):
                for next_position in region_list[index + 1:]:
                    b_eq = self._model.new_bool_var(f"eq_{position.r}_{position.c}_{next_position.r}_{next_position.c}")
                    self._model.Add(self._grid_z3[position] == self._grid_z3[next_position]).OnlyEnforceIf(b_eq)
                    self._model.Add(self._grid_z3[position] != self._grid_z3[next_position]).OnlyEnforceIf(b_eq.Not())
                    b_empty1 = self._model.new_bool_var(f"empty1_{position.r}_{position.c}")
                    self._model.Add(self._grid_z3[position] == self.no_filled_value).OnlyEnforceIf(b_empty1)
                    self._model.Add(self._grid_z3[position] != self.no_filled_value).OnlyEnforceIf(b_empty1.Not())
                    b_empty2 = self._model.new_bool_var(f"empty2_{next_position.r}_{next_position.c}")
                    self._model.Add(self._grid_z3[next_position] == self.no_filled_value).OnlyEnforceIf(b_empty2)
                    self._model.Add(self._grid_z3[next_position] != self.no_filled_value).OnlyEnforceIf(b_empty2.Not())
                    self._model.AddBoolOr([b_eq, b_empty1, b_empty2])

    def _add_count_values(self, positions: Collection[Position]):
        values_z3 = [self._grid_z3[position] for position in positions]
        region_value = max([self._values_grid[position] for position in positions])
        if region_value != self.no_filled_value:
            is_region_val = []
            for position in positions:
                b = self._model.new_bool_var(f"is_region_val_{position.r}_{position.c}")
                self._model.Add(self._grid_z3[position] == region_value).OnlyEnforceIf(b)
                self._model.Add(self._grid_z3[position] != region_value).OnlyEnforceIf(b.Not())
                is_region_val.append(b)
            self._model.Add(sum(is_region_val) == region_value)
        else:
            max_possible = len(positions)
            region_value_z3 = self._model.new_int_var(0, max_possible, f"value_region_{id(positions)}")
            for value_z3 in values_z3:
                self._model.Add(region_value_z3 >= value_z3)
            is_eq = []
            for idx, value_z3 in enumerate(values_z3):
                b = self._model.new_bool_var(f"eq_max_{idx}")
                self._model.Add(region_value_z3 == value_z3).OnlyEnforceIf(b)
                self._model.Add(region_value_z3 != value_z3).OnlyEnforceIf(b.Not())
                is_eq.append(b)
            self._model.AddBoolOr(is_eq)
            is_region_val = []
            for idx, value_z3 in enumerate(values_z3):
                b = self._model.new_bool_var(f"is_region_max_{idx}")
                self._model.Add(value_z3 == region_value_z3).OnlyEnforceIf(b)
                self._model.Add(value_z3 != region_value_z3).OnlyEnforceIf(b.Not())
                is_region_val.append(b)
            self._model.Add(sum(is_region_val) == region_value_z3)

    def _add_no_adjacents_same_values_with_other_regions__constraints(self):
        for region_positions in self._regions_positions_by_id.values():
            self._add_no_adjacents_same_value_with_other_regions_constraints(region_positions)

    def _add_no_adjacents_same_value_with_other_regions_constraints(self, region_positions: Collection[Position]):
        for position in region_positions:
            for neighbor_pos in [neighbor_position for neighbor_position in self._grid_z3.neighbors_positions(position) if neighbor_position not in region_positions]:
                b_diff = self._model.new_bool_var(f"diff_{position.r}_{position.c}_{neighbor_pos.r}_{neighbor_pos.c}")
                self._model.Add(self._grid_z3[position] != self._grid_z3[neighbor_pos]).OnlyEnforceIf(b_diff)
                self._model.Add(self._grid_z3[position] == self._grid_z3[neighbor_pos]).OnlyEnforceIf(b_diff.Not())
                b_empty = self._model.new_bool_var(f"empty_{position.r}_{position.c}")
                self._model.Add(self._grid_z3[position] == self.no_filled_value).OnlyEnforceIf(b_empty)
                self._model.Add(self._grid_z3[position] != self.no_filled_value).OnlyEnforceIf(b_empty.Not())
                self._model.AddBoolOr([b_diff, b_empty])

    def _add_no_isolated_values_constraints(self):
        pass
