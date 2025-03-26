import collections
from typing import Iterable, Set

from z3 import And

from Domain.Direction import Direction
from Domain.Grid.Grid import Grid
from Domain.Ports.SolverEngine import SolverEngine
from Domain.Position import Position
from GameSolver import GameSolver
from Lits.LitsGridBuilder import LitsGridBuilder
from Lits.LitsType import LitsType


class LitsSolver(GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        self._grid = grid
        self._regions = self._grid.get_regions()
        if any(len(region) < 4 for region in self._regions.values()):
            raise ValueError("The grid must have at least 4 cells per region")
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._grid_z3: Grid | None = None
        self.previous_solution: Grid | None = None
        self._solver = solver_engine

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[self._solver.int(f"grid_{r}_{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        self._add_constraints()
        if not self._solver.has_solution():
            return Grid.empty()
        self.previous_solution = Grid([[self._solver.eval(self._grid_z3.value(i, j)) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return self.previous_solution

    def get_other_solution(self):
        exclusion_constraint = self._solver.Not(self._solver.And([self._grid_z3[Position(r, c)] == self.previous_solution[Position(r, c)] for r in range(self.rows_number) for c in range(self.columns_number)]))
        self._solver.add(exclusion_constraint)
        return self.get_solution()

    def _add_constraints(self):
        self._add_range_constraints()
        self._add_count_in_regions_constraints()
        self._add_regions_constraints()
        self._add_no_square_constraints()
        self._add_touching_constraints()

    def _add_range_constraints(self):
        for position, _ in self._grid_z3:
            self._solver.add(self._grid_z3[position] >= 0)
            self._solver.add(self._grid_z3[position] <= max(LitsType, key=lambda x: x.value).value)

    def _add_count_in_regions_constraints(self):
        for region in self._regions.values():
            self._solver.add(self._solver.sum([self._grid_z3[position] != 0 for position in region]) == 4)

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

        constraint = self._solver.Or(*constraints_l, *constraints_i, *constraints_t, *constraints_s)
        self._solver.add(constraint)

    def _get_constraint_for_lits_type(self, region_grid: Grid, offset_position: Position, lits_type: LitsType):
        all_rotation_symetrics_grid = LitsGridBuilder.all(lits_type)
        possible_constraints_l = []
        for grid in all_rotation_symetrics_grid:
            start_positions = grid.find_all_positions_in(region_grid, 0)
            for start_position in start_positions:
                possible_constraint = []
                for position, _ in [(position, value) for position, value in grid if value]:
                    possible_constraint.append(self._grid_z3[position + start_position + offset_position] == lits_type.value)
                possible_constraints_l.append(And(*possible_constraint))
        return possible_constraints_l

    def _add_len4_region_constraints(self, region: Iterable[Position]):
        counter_r = collections.Counter([pos.r for pos in region])
        counter_c = collections.Counter([pos.c for pos in region])

        if len(counter_r) == 1 or len(counter_c) == 1:
            self._solver.add([self._grid_z3[position] == LitsType.I.value for position in region])
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
            self._solver.add([self._grid_z3[position] == LitsType.L.value for position in region])
            return

        if max_counter_c == 3 and counter_r[(min_r + max_r) / 2] == 2 or max_counter_r == 3 and counter_c[(min_c + max_c) / 2] == 2:
            self._solver.add([self._grid_z3[position] == LitsType.T.value for position in region])
            return

        if min_counter_c == 2 and max_counter_c == 2 or min_counter_r == 2 and max_counter_r == 2:
            self._solver.add([self._grid_z3[position] == LitsType.S.value for position in region])
            return

    def _add_no_square_constraints(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                self._solver.add(self._solver.Not(self._solver.And(self._grid_z3[r][c] != 0, self._grid_z3[r + 1][c] != 0, self._grid_z3[r][c + 1] != 0, self._grid_z3[r + 1][c + 1] != 0)))

    def _add_touching_constraints(self):
        adjacent_regions_positions_pairs = self._adjacent_regions_positions_pairs()

        used_pairs = set()
        for region_id, positions_pairs in adjacent_regions_positions_pairs.items():
            region_positions = [positions_pair[0] for positions_pair in positions_pairs]
            self._solver.add(self._solver.sum([self._grid_z3[position] != 0 for position in region_positions]) >= 1)
            for pair in positions_pairs:
                if pair in used_pairs:
                    continue
                used_pairs.add(pair)
                pos0, pos1 = pair
                self._solver.add(self._solver.Or(self._grid_z3[pos0] != self._grid_z3[pos1], self._grid_z3[pos0] == 0, self._grid_z3[pos1] == 0))

    def _adjacent_regions_positions_pairs(self) -> dict[int, Set[tuple[Position, Position]]]:
        adjacents_pairs_dict = collections.defaultdict(set)
        directions = Direction.orthogonals()
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
