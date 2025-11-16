import collections
from typing import Iterable, Set

from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver
from Domain.Puzzles.Lits.LitsGridBuilder import LitsGridBuilder
from Domain.Puzzles.Lits.LitsType import LitsType


class LitsSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self._regions = self._grid.get_regions()
        if any(len(region) < 4 for region in self._regions.values()):
            raise ValueError("The grid must have at least 4 cells per region")
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._grid_vars: Grid | None = None
        self.previous_solution: Grid | None = None
        self._model = cp_model.CpModel()

    def get_solution(self) -> Grid:
        max_value = max(LitsType, key=lambda x: x.value).value
        self._grid_vars = Grid([[self._model.NewIntVar(0, max_value, f"grid_{r}_{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        self._add_constraints()

        solver = cp_model.CpSolver()
        status = solver.Solve(self._model)

        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return Grid.empty()

        self.previous_solution = Grid([[solver.Value(self._grid_vars.value(i, j)) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return self.previous_solution

    def get_other_solution(self):
        if self.previous_solution is None:
            return self.get_solution()

        bool_vars = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                prev_val = self.previous_solution.value(r, c)
                diff_var = self._model.NewBoolVar(f"diff_r{r}_c{c}")
                self._model.Add(self._grid_vars[Position(r, c)] != prev_val).OnlyEnforceIf(diff_var)
                self._model.Add(self._grid_vars[Position(r, c)] == prev_val).OnlyEnforceIf(diff_var.Not())
                bool_vars.append(diff_var)

        self._model.AddBoolOr(bool_vars)

        return self.get_solution()

    def _add_constraints(self):
        self._add_count_in_regions_constraints()
        self._add_regions_constraints()
        self._add_no_square_constraints()
        self._add_touching_constraints()

    def _add_count_in_regions_constraints(self):
        for region in self._regions.values():
            non_zero_cells = []
            for position in region:
                non_zero_cell = self._model.NewBoolVar(f"non_zero_{position.r}_{position.c}")
                self._model.Add(self._grid_vars[position] != 0).OnlyEnforceIf(non_zero_cell)
                self._model.Add(self._grid_vars[position] == 0).OnlyEnforceIf(non_zero_cell.Not())
                non_zero_cells.append(non_zero_cell)
            self._model.Add(sum(non_zero_cells) == 4)

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
        self._model.AddBoolOr(all_constraints)

    def _get_constraint_for_lits_type(self, region_grid: Grid, offset_position: Position, lits_type: LitsType):
        all_rotation_symetrics_grid = LitsGridBuilder.all(lits_type)
        possible_constraints_l = []
        for grid in all_rotation_symetrics_grid:
            start_positions = grid.find_all_positions_in(region_grid, 0)
            for start_position in start_positions:
                config_var = self._model.NewBoolVar(f"config_{lits_type.name}_{start_position.r}_{start_position.c}")

                for position, _ in [(position, value) for position, value in grid if value]:
                    grid_pos = position + start_position + offset_position
                    self._model.Add(self._grid_vars[grid_pos] == lits_type.value).OnlyEnforceIf(config_var)

                possible_constraints_l.append(config_var)
        return possible_constraints_l

    def _add_len4_region_constraints(self, region: Iterable[Position]):
        counter_r = collections.Counter([pos.r for pos in region])
        counter_c = collections.Counter([pos.c for pos in region])

        if len(counter_r) == 1 or len(counter_c) == 1:
            for position in region:
                self._model.Add(self._grid_vars[position] == LitsType.I.value)
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
                self._model.Add(self._grid_vars[position] == LitsType.L.value)
            return

        if max_counter_c == 3 and counter_r[(min_r + max_r) / 2] == 2 or max_counter_r == 3 and counter_c[(min_c + max_c) / 2] == 2:
            for position in region:
                self._model.Add(self._grid_vars[position] == LitsType.T.value)
            return

        if min_counter_c == 2 and max_counter_c == 2 or min_counter_r == 2 and max_counter_r == 2:
            for position in region:
                self._model.Add(self._grid_vars[position] == LitsType.S.value)
            return

    def _add_no_square_constraints(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                top_left = self._model.NewBoolVar(f"non_zero_{r}_{c}")
                top_right = self._model.NewBoolVar(f"non_zero_{r}_{c + 1}")
                bottom_left = self._model.NewBoolVar(f"non_zero_{r + 1}_{c}")
                bottom_right = self._model.NewBoolVar(f"non_zero_{r + 1}_{c + 1}")

                self._model.Add(self._grid_vars[Position(r, c)] != 0).OnlyEnforceIf(top_left)
                self._model.Add(self._grid_vars[Position(r, c)] == 0).OnlyEnforceIf(top_left.Not())

                self._model.Add(self._grid_vars[Position(r, c + 1)] != 0).OnlyEnforceIf(top_right)
                self._model.Add(self._grid_vars[Position(r, c + 1)] == 0).OnlyEnforceIf(top_right.Not())

                self._model.Add(self._grid_vars[Position(r + 1, c)] != 0).OnlyEnforceIf(bottom_left)
                self._model.Add(self._grid_vars[Position(r + 1, c)] == 0).OnlyEnforceIf(bottom_left.Not())

                self._model.Add(self._grid_vars[Position(r + 1, c + 1)] != 0).OnlyEnforceIf(bottom_right)
                self._model.Add(self._grid_vars[Position(r + 1, c + 1)] == 0).OnlyEnforceIf(bottom_right.Not())

                self._model.AddBoolOr([top_left.Not(), top_right.Not(), bottom_left.Not(), bottom_right.Not()])

    def _add_touching_constraints(self):
        adjacent_regions_positions_pairs = self._adjacent_regions_positions_pairs()

        used_pairs = set()
        for region_id, positions_pairs in adjacent_regions_positions_pairs.items():
            region_positions = [positions_pair[0] for positions_pair in positions_pairs]

            non_zero_vars = []
            for position in region_positions:
                non_zero_var = self._model.NewBoolVar(f"non_zero_region_{region_id}_{position.r}_{position.c}")
                self._model.Add(self._grid_vars[position] != 0).OnlyEnforceIf(non_zero_var)
                self._model.Add(self._grid_vars[position] == 0).OnlyEnforceIf(non_zero_var.Not())
                non_zero_vars.append(non_zero_var)

            self._model.AddBoolOr(non_zero_vars)

            for pair in positions_pairs:
                if pair in used_pairs:
                    continue
                used_pairs.add(pair)
                pos0, pos1 = pair

                different_values = self._model.NewBoolVar(f"diff_{pos0.r}_{pos0.c}_{pos1.r}_{pos1.c}")
                pos0_is_zero = self._model.NewBoolVar(f"zero_{pos0.r}_{pos0.c}")
                pos1_is_zero = self._model.NewBoolVar(f"zero_{pos1.r}_{pos1.c}")

                self._model.Add(self._grid_vars[pos0] != self._grid_vars[pos1]).OnlyEnforceIf(different_values)
                self._model.Add(self._grid_vars[pos0] == self._grid_vars[pos1]).OnlyEnforceIf(different_values.Not())

                self._model.Add(self._grid_vars[pos0] == 0).OnlyEnforceIf(pos0_is_zero)
                self._model.Add(self._grid_vars[pos0] != 0).OnlyEnforceIf(pos0_is_zero.Not())

                self._model.Add(self._grid_vars[pos1] == 0).OnlyEnforceIf(pos1_is_zero)
                self._model.Add(self._grid_vars[pos1] != 0).OnlyEnforceIf(pos1_is_zero.Not())

                self._model.AddBoolOr([different_values, pos0_is_zero, pos1_is_zero])

    def _adjacent_regions_positions_pairs(self) -> dict[int, Set[tuple[Position, Position]]]:
        adjacents_pairs_dict = collections.defaultdict(set)
        directions = Direction.orthogonal_directions()
        region_ids = list(self._regions.keys())
        for i, region_id0 in enumerate(region_ids):
            for region_id1 in region_ids[i + 1:]:
                for pos0 in self._regions[region_id0]:
                    for direction in directions:
                        pos1 = pos0.after(direction)
                        if pos1 in self._regions[region_id1]:
                            adjacents_pairs_dict[region_id0].add((pos0, pos1))
                            adjacents_pairs_dict[region_id1].add((pos1, pos0))

        return adjacents_pairs_dict
