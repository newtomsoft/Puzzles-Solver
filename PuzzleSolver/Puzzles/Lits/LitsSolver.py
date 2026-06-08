import collections
from typing import Iterable

from ortools.sat.python import cp_model

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver
from PuzzleSolver.Puzzles.Lits.LitsGridBuilder import LitsGridBuilder
from PuzzleSolver.Puzzles.Lits.LitsType import LitsType


class LitsSolver(GameSolver):
    cell_empty = 0

    def __init__(self, grid: Grid):
        super().__init__()
        self._grid = grid
        self._regions = self._grid.get_regions()
        if any(len(region) < 4 for region in self._regions.values()):
            raise ValueError("The grid must have at least 4 cells per region")
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._grid_vars = Grid.empty()
        self._shaded_vars = Grid.empty()
        self.previous_solution = Grid.empty()
        self._model = cp_model.CpModel()

    def get_solution(self) -> Grid:
        if self._grid_vars.is_empty():
            self._init_solver()

        status = self._solver.solve(self._model)
        if status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return Grid.empty()

        current_solution = Grid([[self._solver.value(self._grid_vars.value(i, j)) for j in range(self.columns_number)] for i in range(self.rows_number)])
        self.previous_solution = current_solution
        return current_solution

    def _init_solver(self):
        max_value = max(LitsType, key=lambda x: x.value).value
        self._grid_vars = Grid([[self._model.new_int_var(0, max_value, f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._shaded_vars = Grid([[self._model.new_bool_var(f"shaded_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])

        for pos, value in self._grid_vars:
            self._model.add(value != 0).only_enforce_if(self._shaded_vars[pos])
            self._model.add(value == 0).only_enforce_if(self._shaded_vars[pos].negated())

        self._add_constraints()

    def get_other_solution(self):
        bool_vars = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                prev_val = self.previous_solution.value(r, c)
                diff_var = self._model.new_bool_var(f"diff_r{r}_c{c}_{len(self._model.Proto().variables)}")
                self._model.add(self._grid_vars[Position(r, c)] != prev_val).only_enforce_if(diff_var)
                self._model.add(self._grid_vars[Position(r, c)] == prev_val).only_enforce_if(diff_var.negated())
                bool_vars.append(diff_var)

        self._model.add_bool_or(bool_vars)

        return self.get_solution()

    def _add_constraints(self):
        self._add_count_in_regions_constraints()
        self._add_regions_constraints()
        self._add_no_square_constraints()
        self._add_touching_constraints()
        self._add_shaded_connectivity_constraint()

    def _add_shaded_connectivity_constraint(self):
        total_cells = self.rows_number * self.columns_number
        self._rank_vars = Grid([[self._model.new_int_var(0, total_cells - 1, f"rank_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        is_root_vars = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                is_root = self._model.new_bool_var(f"is_root_{r}_{c}")
                is_root_vars.append(is_root)
                is_shaded = self._shaded_vars[pos]
                self._model.add(is_root <= is_shaded)
                self._model.add(self._rank_vars[pos] == 0).OnlyEnforceIf(is_root)
        self._model.add(sum(is_root_vars) == 1)
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                is_shaded = self._shaded_vars[pos]
                is_root = is_root_vars[r * self.columns_number + c]
                parent_literals = []
                for neighbor in self._shaded_vars.neighbors_positions(pos):
                    parent = self._model.new_bool_var(f"parent_{r}_{c}_{neighbor.r}_{neighbor.c}")
                    self._model.add(self._shaded_vars[neighbor] == 1).OnlyEnforceIf(parent)
                    self._model.add(self._rank_vars[neighbor] < self._rank_vars[pos]).OnlyEnforceIf(parent)
                    parent_literals.append(parent)
                if parent_literals:
                    self._model.add_bool_or(parent_literals).OnlyEnforceIf([is_shaded, is_root.negated()])

    def _add_count_in_regions_constraints(self):
        for region in self._regions.values():
            self._model.add(sum(self._shaded_vars[pos] for pos in region) == 4)

    def _add_regions_constraints(self):
        for region in self._regions.values():
            self._add_region_constraints(region)

    def _add_region_constraints(self, region: frozenset[Position]):
        if len(region) == 4:
            self._add_len4_region_constraints(region)
            return

        region_grid, offset_position = Grid.from_positions(region, 1, 0)

        constraints_l = self._get_constraint_for_lits_type(region_grid, offset_position, LitsType.L)
        constraints_i = self._get_constraint_for_lits_type(region_grid, offset_position, LitsType.I)
        constraints_t = self._get_constraint_for_lits_type(region_grid, offset_position, LitsType.T)
        constraints_s = self._get_constraint_for_lits_type(region_grid, offset_position, LitsType.S)

        all_constraints = constraints_l + constraints_i + constraints_t + constraints_s
        self._model.add_bool_or(all_constraints)

    def _get_constraint_for_lits_type(self, region_grid: Grid, offset_position: Position, lits_type: LitsType):
        all_rotation_symetrics_grid = LitsGridBuilder.all(lits_type)
        possible_constraints = []
        for grid in all_rotation_symetrics_grid:
            start_positions = grid.find_all_positions_in(region_grid, 0)
            for start_position in start_positions:
                config_var = self._model.new_bool_var(f"config_{lits_type.name}_{start_position.r}_{start_position.c}")
                possible_constraints.append(config_var)
                for position in [position for position, value in grid if value]:
                    grid_pos = position + start_position + offset_position
                    self._model.add(self._grid_vars[grid_pos] == lits_type.value).only_enforce_if(config_var)
                    self._model.add(self._shaded_vars[grid_pos] == 1).only_enforce_if(config_var)

        return possible_constraints

    def _add_len4_region_constraints(self, region: Iterable[Position]):
        counter_r = collections.Counter([pos.r for pos in region])
        counter_c = collections.Counter([pos.c for pos in region])

        if len(counter_r) == 1 or len(counter_c) == 1:
            for position in region:
                self._model.add(self._grid_vars[position] == LitsType.I.value)
            return

        min_counter_c = min(counter_c.values())
        max_counter_c = max(counter_c.values())
        min_counter_r = min(counter_r.values())
        max_counter_r = max(counter_r.values())
        min_c = min(position.c for position in region)
        max_c = max(position.c for position in region)
        min_r = min(position.r for position in region)
        max_r = max(position.r for position in region)

        if max_counter_c == 3 and (counter_r[min_r] == 2 or counter_r[max_r] == 2) or max_counter_r == 3 and (counter_c[min_c] == 2 or counter_c[max_c] == 2):
            for position in region:
                self._model.add(self._grid_vars[position] == LitsType.L.value)
            return

        if max_counter_c == 3 and counter_r[(min_r + max_r) / 2] == 2 or max_counter_r == 3 and counter_c[(min_c + max_c) / 2] == 2:
            for position in region:
                self._model.add(self._grid_vars[position] == LitsType.T.value)
            return

        if min_counter_c == 2 and max_counter_c == 2 or min_counter_r == 2 and max_counter_r == 2:
            for position in region:
                self._model.add(self._grid_vars[position] == LitsType.S.value)
            return

    def _add_no_square_constraints(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                self._model.add(
                    self._shaded_vars[Position(r, c)] +
                    self._shaded_vars[Position(r, c + 1)] +
                    self._shaded_vars[Position(r + 1, c)] +
                    self._shaded_vars[Position(r + 1, c + 1)] < 4
                )

    def _add_touching_constraints(self):
        adjacent_regions_positions_pairs = self._adjacent_regions_positions_pairs()

        for region_id, positions_pairs in adjacent_regions_positions_pairs.items():
            region_positions = {pair[0] for pair in positions_pairs}
            self._model.add_bool_or([self._shaded_vars[pos] for pos in region_positions])

        used_pairs = set()
        for region_id, positions_pairs in adjacent_regions_positions_pairs.items():
            for pair in positions_pairs:
                pos0, pos1 = pair
                if (pos1, pos0) in used_pairs:
                    continue
                used_pairs.add(pair)

                different_values = self._model.new_bool_var(f"diff_{pos0.r}_{pos0.c}_{pos1.r}_{pos1.c}")
                self._model.add(self._grid_vars[pos0] != self._grid_vars[pos1]).only_enforce_if(different_values)
                self._model.add(self._grid_vars[pos0] == self._grid_vars[pos1]).only_enforce_if(different_values.negated())
                self._model.add_bool_or([self._shaded_vars[pos0].negated(), self._shaded_vars[pos1].negated(), different_values])

    def _adjacent_regions_positions_pairs(self) -> dict[int, set[tuple[Position, Position]]]:
        adjacents_pairs_dict = collections.defaultdict(set)
        directions = Direction.orthogonal_directions()

        pos_to_region = {}
        for region_id, positions in self._regions.items():
            for pos in positions:
                pos_to_region[pos] = region_id

        for pos0, region_id0 in pos_to_region.items():
            for direction in directions:
                pos1 = pos0.after(direction)
                if pos1 in pos_to_region:
                    region_id1 = pos_to_region[pos1]
                    if region_id0 != region_id1:
                        adjacents_pairs_dict[region_id0].add((pos0, pos1))

        return adjacents_pairs_dict
