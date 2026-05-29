from ortools.sat.python import cp_model

from Domain.Board import RegionsGrid
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
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

    def __init__(self, clues_clues_grid: Grid):
        self._clues_grid = clues_clues_grid
        self._rows_number = clues_clues_grid.rows_number
        self._columns_number = clues_clues_grid.columns_number
        self._model = cp_model.CpModel()
        self._grid_ortools: Grid | None = None
        self._clue_by_position = dict([(position, value) for position, value in self._clues_grid if value != NeighboursSolver.empty])
        self._clue_position_by_region_id = {index + 1: position for index, position in enumerate(self._clue_by_position.keys())}
        self._regions_count = len(self._clue_by_position)
        self._solver = cp_model.CpSolver()

    def get_solution(self) -> RegionsGrid:
        self._grid_ortools = Grid([[self._model.new_int_var(1, self._regions_count, f"grid_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()
        return self._compute_solution()

    def get_other_solution(self) -> RegionsGrid:
        bool_vars = []
        for position, value in self._previous_solution:
            b = self._model.new_bool_var('')
            self._model.add(self._grid_ortools[position] != value).only_enforce_if(b)
            self._model.add(self._grid_ortools[position] == value).only_enforce_if(b.Not())
            bool_vars.append(b)
        self._model.add(sum(bool_vars) > 0)
        return self._compute_solution()

    def _compute_solution(self) -> RegionsGrid:
        status = self._solver.solve(self._model)
        if status == cp_model.INFEASIBLE or status == cp_model.UNKNOWN:
            return Grid.empty()
        solution = Grid([[self._solver.value(self._grid_ortools.value(i, j)) for j in range(self._columns_number)] for i in range(self._rows_number)])
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
        area = self._rows_number * self._columns_number // self._regions_count
        for region_id in self._clue_position_by_region_id.keys():
            bool_vars = []
            for position, _ in self._clues_grid:
                b = self._model.new_bool_var('')
                self._model.add(self._grid_ortools[position] == region_id).only_enforce_if(b)
                self._model.add(self._grid_ortools[position] != region_id).only_enforce_if(b.Not())
                bool_vars.append(b)
            self._model.add(sum(bool_vars) == area)

    def _add_connected_cells_regions_constraints(self):
        area = self._rows_number * self._columns_number // self._regions_count
        if area in self.SHAPES:
            for region_id in self._clue_position_by_region_id.keys():
                self._add_shape_based_connectivity_constraint(region_id, area)
        else:
            steps = [Grid([[self._model.new_int_var(0, self._rows_number * self._columns_number, f'step{region_id}_{r}_{c}')
                            for c in range(self._columns_number)] for r in range(self._rows_number)]) for region_id in
                     range(1, self._regions_count + 1)]
            for region_id in self._clue_position_by_region_id.keys():
                self._add_connected_cells_region_constraints(steps[region_id - 1], region_id)

    def _add_connected_cells_region_constraints(self, step: Grid, region_id: int):
        is_in_region = {}
        for pos, _ in self._clues_grid:
            b = self._model.new_bool_var(f'is_in_region_{region_id}_{pos.r}_{pos.c}')
            self._model.add(self._grid_ortools[pos] == region_id).only_enforce_if(b)
            self._model.add(self._grid_ortools[pos] != region_id).only_enforce_if(b.Not())
            is_in_region[pos] = b

        for position, _ in self._clues_grid:
            self._model.add(step[position] >= 1).only_enforce_if(is_in_region[position])
            self._model.add(step[position] == 0).only_enforce_if(is_in_region[position].Not())

        roots = []
        for position, _ in self._clues_grid:
            is_root = self._model.new_bool_var(f'root_{region_id}_{position.r}_{position.c}')
            is_step_one = self._model.new_bool_var(f'step_is_one_{region_id}_{position.r}_{position.c}')
            self._model.add(step[position] == 1).only_enforce_if(is_step_one)
            self._model.add(step[position] != 1).only_enforce_if(is_step_one.Not())
            self._model.add_implication(is_root, is_in_region[position])
            self._model.add_implication(is_root, is_step_one)
            self._model.add_bool_or([is_in_region[position].Not(), is_step_one.Not(), is_root])
            roots.append(is_root)
        self._model.add(sum(roots) == 1)

        for r in range(self._rows_number):
            for c in range(self._columns_number):
                pos = Position(r, c)
                current_step = step[pos]

                is_step_gt_1 = self._model.new_bool_var(f"step_gt_1_{region_id}_{r}_{c}")
                self._model.add(current_step > 1).only_enforce_if(is_step_gt_1)
                self._model.add(current_step <= 1).only_enforce_if(is_step_gt_1.Not())

                implication_condition = self._model.new_bool_var(f"impl_cond_{region_id}_{r}_{c}")
                self._model.add_implication(implication_condition, is_in_region[pos])
                self._model.add_implication(implication_condition, is_step_gt_1)
                self._model.add_bool_or([is_in_region[pos].Not(), is_step_gt_1.Not(), implication_condition])

                adjacents_ok = []
                for neighbor_pos in self._clues_grid.neighbors_positions(pos):
                    is_neighbor_step_parent = self._model.new_bool_var(f'parent_{region_id}_{neighbor_pos.r}_{neighbor_pos.c}')
                    self._model.add(step[neighbor_pos] == current_step - 1).only_enforce_if(is_neighbor_step_parent)
                    self._model.add(step[neighbor_pos] != current_step - 1).only_enforce_if(is_neighbor_step_parent.Not())

                    b_adj = self._model.new_bool_var(f'adj_{region_id}_{neighbor_pos.r}_{neighbor_pos.c}')
                    self._model.add_implication(b_adj, is_in_region[neighbor_pos])
                    self._model.add_implication(b_adj, is_neighbor_step_parent)
                    self._model.add_bool_or([is_in_region[neighbor_pos].Not(), is_neighbor_step_parent.Not(), b_adj])
                    adjacents_ok.append(b_adj)

                if adjacents_ok:
                    self._model.add_bool_or(adjacents_ok).only_enforce_if(implication_condition)

    def _add_shape_based_connectivity_constraint(self, region_id: int, area: int):
        possible_placements = []
        is_in_region_vars = {(r, c): self._model.new_bool_var(f'is_in_region_{region_id}_{r}_{c}')
                             for r in range(self._rows_number) for c in range(self._columns_number)}

        for r in range(self._rows_number):
            for c in range(self._columns_number):
                self._model.add(self._grid_ortools[r][c] == region_id).only_enforce_if(is_in_region_vars[(r, c)])
                self._model.add(self._grid_ortools[r][c] != region_id).only_enforce_if(is_in_region_vars[(r, c)].Not())

        for s_idx, shape in enumerate(self.SHAPES[area]):
            for r_offset in range(self._rows_number):
                for c_offset in range(self._columns_number):
                    placement_positions = [Position(r_offset + p.r, c_offset + p.c) for p in shape]

                    if self._clues_grid.are_valid_positions(placement_positions):
                        placement_bool = self._model.new_bool_var(f'placement_{region_id}_{s_idx}_{r_offset}_{c_offset}')
                        possible_placements.append(placement_bool)

                        cell_bools = [is_in_region_vars[(p.r, p.c)] for p in placement_positions]
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
        for i in region_ids:
            for j in region_ids:
                if i >= j:
                    continue

                adj_bool = self._model.new_bool_var(f'adj_{i}_{j}')

                edge_connects_ij_bools = []
                for u, v in adjacent_edges:
                    b_edge = self._model.new_bool_var(f'edge_{u.r}{u.c}_{v.r}{v.c}_connects_{i}{j}')

                    b_ui = self._model.new_bool_var(f'b_{u.r}{u.c}=={i}')
                    self._model.add(self._grid_ortools[u] == i).only_enforce_if(b_ui)
                    self._model.add(self._grid_ortools[u] != i).only_enforce_if(b_ui.Not())

                    b_vj = self._model.new_bool_var(f'b_{v.r}{v.c}=={j}')
                    self._model.add(self._grid_ortools[v] == j).only_enforce_if(b_vj)
                    self._model.add(self._grid_ortools[v] != j).only_enforce_if(b_vj.Not())

                    b_uj = self._model.new_bool_var(f'b_{u.r}{u.c}=={j}')
                    self._model.add(self._grid_ortools[u] == j).only_enforce_if(b_uj)
                    self._model.add(self._grid_ortools[u] != j).only_enforce_if(b_uj.Not())

                    b_vi = self._model.new_bool_var(f'b_{v.r}{v.c}=={i}')
                    self._model.add(self._grid_ortools[v] == i).only_enforce_if(b_vi)
                    self._model.add(self._grid_ortools[v] != i).only_enforce_if(b_vi.Not())

                    b_term1 = self._model.new_bool_var(f'b_term1_{u.r}{u.c}_{v.r}{v.c}_{i}{j}')
                    self._model.add_implication(b_term1, b_ui)
                    self._model.add_implication(b_term1, b_vj)
                    self._model.add_bool_or([b_ui.Not(), b_vj.Not(), b_term1])

                    b_term2 = self._model.new_bool_var(f'b_term2_{u.r}{u.c}_{v.r}{v.c}_{i}{j}')
                    self._model.add_implication(b_term2, b_uj)
                    self._model.add_implication(b_term2, b_vi)
                    self._model.add_bool_or([b_uj.Not(), b_vi.Not(), b_term2])

                    self._model.add_implication(b_term1, b_edge)
                    self._model.add_implication(b_term2, b_edge)
                    self._model.add_bool_or([b_term1, b_term2, b_edge.Not()])

                    edge_connects_ij_bools.append(b_edge)

                if edge_connects_ij_bools:
                    self._model.add_bool_or(edge_connects_ij_bools).only_enforce_if(adj_bool)
                    for b in edge_connects_ij_bools:
                        self._model.add_implication(b, adj_bool)
                else:
                    self._model.add(adj_bool == 0)

                adj_between_regions[(i, j)] = adj_bool

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
