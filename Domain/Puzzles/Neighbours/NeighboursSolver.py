from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Board.RegionsGrid import RegionsGrid
from Domain.Puzzles.GameSolver import GameSolver


class NeighboursSolver(GameSolver):
    empty = None
    unknow = 0
    SHAPES = {
        2: [
            [Position(0, 0), Position(0, 1)],
            [Position(0, 0), Position(1, 0)],
        ],
        3: [
            [Position(0, 0), Position(0, 1), Position(0, 2)],
            [Position(0, 0), Position(1, 0), Position(2, 0)],
            [Position(0, 0), Position(0, 1), Position(1, 0)],
            [Position(0, 0), Position(0, 1), Position(1, 1)],
            [Position(0, 0), Position(1, 0), Position(1, 1)],
            [Position(0, 1), Position(1, 0), Position(1, 1)],
        ],
        4: [
            [Position(0, 0), Position(0, 1), Position(0, 2), Position(0, 3)],
            [Position(0, 0), Position(1, 0), Position(2, 0), Position(3, 0)],
            [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)],
            [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],
            [Position(0, 0), Position(1, 0), Position(2, 0), Position(1, 1)],
            [Position(1, 0), Position(0, 1), Position(1, 1), Position(2, 1)],
            [Position(0, 1), Position(1, 1), Position(2, 1), Position(1, 0)],
            [Position(0, 0), Position(1, 0), Position(2, 0), Position(2, 1)],
            [Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],
            [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1)],
            [Position(0, 0), Position(1, 0), Position(0, 1), Position(0, 2)],
            [Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 0)],
            [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
            [Position(0, 0), Position(1, 0), Position(2, 0), Position(0, 1)],
            [Position(0, 2), Position(0, 0), Position(0, 1), Position(1, 2)],
            [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],
            [Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1)],
            [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],
            [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)],
        ],
    }

    def __init__(self, clues_grid: Grid):
        self._clues_grid = clues_grid
        self._rows_number = clues_grid.rows_number
        self._columns_number = clues_grid.columns_number
        self._model = cp_model.CpModel()
        self._grid_ortools: Grid | None = None
        self._clue_by_position = dict([(position, value) for position, value in self._clues_grid if value != NeighboursSolver.empty])
        self._clue_position_by_region_id = {index + 1: position for index, position in enumerate(self._clue_by_position.keys())}
        self._regions_count = len(self._clue_by_position)
        self._solver = cp_model.CpSolver()
        self._area = self._rows_number * self._columns_number // self._regions_count
        self._possible_positions_by_region_id = {}
        for region_id, root in self._clue_position_by_region_id.items():
            possible = []
            for r in range(max(0, root.r - self._area + 1), min(self._rows_number, root.r + self._area)):
                for c in range(max(0, root.c - self._area + 1), min(self._columns_number, root.c + self._area)):
                    pos = Position(r, c)
                    if abs(pos.r - root.r) + abs(pos.c - root.c) < self._area:
                        possible.append(pos)
            self._possible_positions_by_region_id[region_id] = possible

        self._possible_regions_by_position = {}
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                pos = Position(r, c)
                self._possible_regions_by_position[pos] = [
                    region_id for region_id, positions in self._possible_positions_by_region_id.items()
                    if pos in positions
                ]

        self._is_in_region_vars = {}

    def _get_is_in_region_var(self, region_id: int, pos: Position):
        if (region_id, pos) not in self._is_in_region_vars:
            if region_id not in self._possible_regions_by_position[pos]:
                self._is_in_region_vars[(region_id, pos)] = self._model.new_constant(0)
            else:
                b = self._model.new_bool_var(f'is_in_region_{region_id}_{pos.r}_{pos.c}')
                self._model.add(self._grid_ortools[pos] == region_id).only_enforce_if(b)
                self._model.add(self._grid_ortools[pos] != region_id).only_enforce_if(b.negated())
                self._is_in_region_vars[(region_id, pos)] = b
        return self._is_in_region_vars[(region_id, pos)]

    def get_solution(self) -> Grid:
        grid_vars = []
        for r in range(self._rows_number):
            row_vars = []
            for c in range(self._columns_number):
                pos = Position(r, c)
                possible_regions = self._possible_regions_by_position[pos]
                var = self._model.new_int_var_from_domain(cp_model.Domain.from_values(possible_regions), f"grid_{r}_{c}")
                row_vars.append(var)
            grid_vars.append(row_vars)
        self._grid_ortools = Grid(grid_vars)
        self._add_constraints()
        return self._compute_solution()

    def get_other_solution(self) -> Grid:
        bool_vars = []
        for position, value in self._previous_solution:
            b = self._model.new_bool_var('')
            self._model.add(self._grid_ortools[position] != value).only_enforce_if(b)
            self._model.add(self._grid_ortools[position] == value).only_enforce_if(b.negated())
            bool_vars.append(b)
        self._model.add(sum(bool_vars) > 0)
        return self._compute_solution()

    def _compute_solution(self) -> Grid:
        status = self._solver.solve(self._model)
        if status == cp_model.INFEASIBLE or status == cp_model.UNKNOWN:
            return Grid.empty()
        solution = RegionsGrid([[self._solver.value(self._grid_ortools.value(i, j)) for j in range(self._columns_number)] for i in range(self._rows_number)])
        self._previous_solution = solution
        return solution

    def _add_constraints(self):
        self._add_initials_constraints()
        self._add_area_regions_constraints()
        self._add_connected_cells_regions_constraints()
        self._add_neighbours_clues_constraints()

    def _add_initials_constraints(self):
        for region_id, position in self._clue_position_by_region_id.items():
            self._model.add(self._grid_ortools[position] == region_id)

    def _add_area_regions_constraints(self):
        for region_id in self._clue_position_by_region_id.keys():
            bool_vars = [self._get_is_in_region_var(region_id, pos) for pos in self._possible_positions_by_region_id[region_id]]
            self._model.add(sum(bool_vars) == self._area)

    def _add_connected_cells_regions_constraints(self):
        for region_id in self._clue_position_by_region_id.keys():
            step = Grid([[self._model.new_int_var(0, self._area, f'step{region_id}_{r}_{c}')
                          if Position(r, c) in self._possible_positions_by_region_id[region_id] else self._model.new_constant(0)
                          for c in range(self._columns_number)] for r in range(self._rows_number)])
            self._add_connected_cells_region_constraints(step, region_id)

    def _add_connected_cells_region_constraints(self, step: Grid, region_id: int):
        possible_positions = self._possible_positions_by_region_id[region_id]
        is_in_region = {pos: self._get_is_in_region_var(region_id, pos) for pos in possible_positions}

        for position in possible_positions:
            self._model.add(step[position] >= 1).only_enforce_if(is_in_region[position])
            self._model.add(step[position] == 0).only_enforce_if(is_in_region[position].negated())

        roots = []
        clue_pos = self._clue_position_by_region_id[region_id]
        for position in possible_positions:
            is_step_one = self._model.new_bool_var(f'step_is_one_{region_id}_{position.r}_{position.c}')
            self._model.add(step[position] == 1).only_enforce_if(is_step_one)
            self._model.add(step[position] != 1).only_enforce_if(is_step_one.negated())
            if position == clue_pos:
                self._model.add(is_step_one == 1)
            else:
                self._model.add(is_step_one == 0)

        for pos in possible_positions:
            r, c = pos.r, pos.c
            current_step = step[pos]

            if pos == clue_pos:
                continue

            # If cell is in region, it must have a parent (current_step > 1 and neighbor has current_step - 1)
            # This is only possible if current_step > 1.
            self._model.add(current_step > 1).only_enforce_if(is_in_region[pos])

            adjacents_ok = []
            for neighbor_pos in self._clues_grid.neighbors_positions(pos):
                if neighbor_pos not in possible_positions:
                    continue
                
                is_parent = self._model.new_bool_var(f'parent_{region_id}_{pos.r}_{pos.c}_{neighbor_pos.r}_{neighbor_pos.c}')
                # neighbor is parent if it's in the region and has step = current_step - 1
                self._model.add(step[neighbor_pos] == current_step - 1).only_enforce_if(is_parent)
                self._model.add(step[neighbor_pos] != current_step - 1).only_enforce_if(is_parent.negated())
                
                b_parent_ok = self._model.new_bool_var('')
                self._model.add_bool_and([is_in_region[neighbor_pos], is_parent]).only_enforce_if(b_parent_ok)
                adjacents_ok.append(b_parent_ok)

            if adjacents_ok:
                self._model.add_bool_or(adjacents_ok).only_enforce_if(is_in_region[pos])
            else:
                self._model.add(is_in_region[pos] == 0)

    def _add_shape_based_connectivity_constraint(self, region_id: int, area: int):
        possible_placements = []
        possible_positions = self._possible_positions_by_region_id[region_id]

        for s_idx, shape in enumerate(self.SHAPES[area]):
            # Optimization: only iterate over offsets that could possibly fit the shape within the allowed positions
            for r_offset in range(self._rows_number):
                for c_offset in range(self._columns_number):
                    placement_positions = [Position(r_offset + p.r, c_offset + p.c) for p in shape]

                    if self._clues_grid.are_valid_positions(placement_positions) and all(p in possible_positions for p in placement_positions):
                        placement_bool = self._model.new_bool_var(f'placement_{region_id}_{s_idx}_{r_offset}_{c_offset}')
                        possible_placements.append(placement_bool)

                        cell_bools = [self._get_is_in_region_var(region_id, p) for p in placement_positions]
                        self._model.add_bool_and(cell_bools).only_enforce_if(placement_bool)

        self._model.add(sum(possible_placements) == 1)

    def _add_neighbours_clues_constraints(self):
        adjacent_edges: list[tuple[Position, Position]] = []
        for position, _ in self._clues_grid:
            for neighbor in self._clues_grid.neighbors_positions(position):
                if position < neighbor:
                    adjacent_edges.append((position, neighbor))

        region_ids = list(self._clue_position_by_region_id.keys())
        adj_between_regions: dict[tuple[int, int], cp_model.BoolVarT] = {}

        # 1. Filter possible adjacencies between regions based on root distance
        possible_adj_pairs = []
        for idx, i in enumerate(region_ids):
            for j in region_ids[idx + 1:]:
                root_i = self._clue_position_by_region_id[i]
                root_j = self._clue_position_by_region_id[j]
                # Maximum distance for two regions to be adjacent is 2 * (area - 1) + 1
                if abs(root_i.r - root_j.r) + abs(root_i.c - root_j.c) <= 2 * self._area - 1:
                    possible_adj_pairs.append((i, j))
                else:
                    adj_between_regions[(i, j)] = self._model.new_constant(0)

        # 2. For each possible pair, find if they are adjacent
        # Pre-filter edges by region pair
        edges_by_region_pair = {}
        for u, v in adjacent_edges:
            regs_u = self._possible_regions_by_position[u]
            regs_v = self._possible_regions_by_position[v]
            for ri in regs_u:
                for rj in regs_v:
                    if ri == rj: continue
                    pair = (ri, rj) if ri < rj else (rj, ri)
                    if pair not in edges_by_region_pair:
                        edges_by_region_pair[pair] = []
                    # Keep track of which region is at which position
                    edges_by_region_pair[pair].append((u, v, ri, rj))

        for i, j in possible_adj_pairs:
            adj_bool = self._model.new_bool_var(f'adj_{i}_{j}')
            adj_between_regions[(i, j)] = adj_bool
            
            all_term_bools = []
            for u, v, ri, rj in edges_by_region_pair.get((i, j), []):
                b_uri = self._get_is_in_region_var(ri, u)
                b_vrj = self._get_is_in_region_var(rj, v)
                
                # Force adj_bool to 1 if these cells are ri and rj
                self._model.add(adj_bool == 1).only_enforce_if([b_uri, b_vrj])
                
                # Variable to justify adj_bool == 1
                b_term = self._model.new_bool_var('')
                self._model.add_bool_and([b_uri, b_vrj]).only_enforce_if(b_term)
                all_term_bools.append(b_term)

            if not all_term_bools:
                self._model.add(adj_bool == 0)
            else:
                self._model.add_bool_or(all_term_bools).only_enforce_if(adj_bool)

        # 3. Clue constraints
        for i in region_ids:
            clue_position = self._clue_position_by_region_id[i]
            clue_value = self._clue_by_position[clue_position]
            if clue_value == self.unknow:
                continue
            terms = []
            for j in region_ids:
                if i == j:
                    continue
                key = (i, j) if i < j else (j, i)
                terms.append(adj_between_regions[key])
            self._model.add(sum(terms) == clue_value)
