from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class NeighboursSolver(GameSolver):
    empty = None
    unknow = 0

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

    def get_solution(self) -> Grid:
        self._grid_ortools = Grid([[self._model.NewIntVar(1, self._regions_count, f"grid_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()
        return self._compute_solution()

    def get_other_solution(self) -> Grid:
        bool_vars = []
        for position, value in self._previous_solution:
            b = self._model.NewBoolVar('')
            self._model.Add(self._grid_ortools[position] != value).OnlyEnforceIf(b)
            self._model.Add(self._grid_ortools[position] == value).OnlyEnforceIf(b.Not())
            bool_vars.append(b)
        self._model.Add(sum(bool_vars) > 0)
        return self._compute_solution()

    def _compute_solution(self) -> Grid:
        status = self._solver.Solve(self._model)
        if status == cp_model.INFEASIBLE or status == cp_model.UNKNOWN:
            return Grid.empty()
        solution = Grid([[self._solver.Value(self._grid_ortools.value(i, j)) for j in range(self._columns_number)] for i in range(self._rows_number)])
        self._previous_solution = solution
        return solution

    def _add_constraints(self):
        self._add_initials_constraints()
        self._add_area_regions_constraints()
        self._add_connected_cells_regions_constraints()
        self._add_neighbours_clues_constraints()

    def _add_initials_constraints(self):
        for region_id, position in self._clue_position_by_region_id.items():
            self._model.Add(self._grid_ortools[position] == region_id)

    def _add_area_regions_constraints(self):
        area = self._rows_number * self._columns_number // self._regions_count
        for region_id in self._clue_position_by_region_id.keys():
            bool_vars = []
            for position, _ in self._clues_grid:
                b = self._model.NewBoolVar('')
                self._model.Add(self._grid_ortools[position] == region_id).OnlyEnforceIf(b)
                self._model.Add(self._grid_ortools[position] != region_id).OnlyEnforceIf(b.Not())
                bool_vars.append(b)
            self._model.Add(sum(bool_vars) == area)

    def _add_connected_cells_regions_constraints(self):
        steps = [Grid([[self._model.NewIntVar(0, self._rows_number * self._columns_number, f'step{region_id}_{r}_{c}')
                        for c in range(self._columns_number)] for r in range(self._rows_number)]) for region_id in
                 range(1, self._regions_count + 1)]
        for region_id in self._clue_position_by_region_id.keys():
            self._add_connected_cells_region_constraints(steps[region_id - 1], region_id)

    def _add_connected_cells_region_constraints(self, step: Grid, region_id: int):
        is_in_region = {}
        for pos, _ in self._clues_grid:
            b = self._model.NewBoolVar(f'is_in_region_{region_id}_{pos.r}_{pos.c}')
            self._model.Add(self._grid_ortools[pos] == region_id).OnlyEnforceIf(b)
            self._model.Add(self._grid_ortools[pos] != region_id).OnlyEnforceIf(b.Not())
            is_in_region[pos] = b

        for position, _ in self._clues_grid:
            self._model.Add(step[position] >= 1).OnlyEnforceIf(is_in_region[position])
            self._model.Add(step[position] == 0).OnlyEnforceIf(is_in_region[position].Not())

        roots = []
        for position, _ in self._clues_grid:
            is_root = self._model.NewBoolVar(f'root_{region_id}_{position.r}_{position.c}')
            is_step_one = self._model.NewBoolVar(f'step_is_one_{region_id}_{position.r}_{position.c}')
            self._model.Add(step[position] == 1).OnlyEnforceIf(is_step_one)
            self._model.Add(step[position] != 1).OnlyEnforceIf(is_step_one.Not())
            self._model.AddImplication(is_root, is_in_region[position])
            self._model.AddImplication(is_root, is_step_one)
            self._model.AddBoolOr([is_in_region[position].Not(), is_step_one.Not(), is_root])
            roots.append(is_root)
        self._model.Add(sum(roots) == 1)

        for r in range(self._rows_number):
            for c in range(self._columns_number):
                pos = Position(r, c)
                current_step = step[pos]

                is_step_gt_1 = self._model.NewBoolVar(f"step_gt_1_{region_id}_{r}_{c}")
                self._model.Add(current_step > 1).OnlyEnforceIf(is_step_gt_1)
                self._model.Add(current_step <= 1).OnlyEnforceIf(is_step_gt_1.Not())

                implication_condition = self._model.NewBoolVar(f"impl_cond_{region_id}_{r}_{c}")
                self._model.AddImplication(implication_condition, is_in_region[pos])
                self._model.AddImplication(implication_condition, is_step_gt_1)
                self._model.AddBoolOr([is_in_region[pos].Not(), is_step_gt_1.Not(), implication_condition])

                adjacents_ok = []
                for neighbor_pos in self._clues_grid.neighbors_positions(pos):
                    is_neighbor_step_parent = self._model.NewBoolVar(f'parent_{region_id}_{neighbor_pos.r}_{neighbor_pos.c}')
                    self._model.Add(step[neighbor_pos] == current_step - 1).OnlyEnforceIf(is_neighbor_step_parent)
                    self._model.Add(step[neighbor_pos] != current_step - 1).OnlyEnforceIf(is_neighbor_step_parent.Not())

                    b_adj = self._model.NewBoolVar(f'adj_{region_id}_{neighbor_pos.r}_{neighbor_pos.c}')
                    self._model.AddImplication(b_adj, is_in_region[neighbor_pos])
                    self._model.AddImplication(b_adj, is_neighbor_step_parent)
                    self._model.AddBoolOr([is_in_region[neighbor_pos].Not(), is_neighbor_step_parent.Not(), b_adj])
                    adjacents_ok.append(b_adj)

                if adjacents_ok:
                    self._model.AddBoolOr(adjacents_ok).OnlyEnforceIf(implication_condition)

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

                adj_bool = self._model.NewBoolVar(f'adj_{i}_{j}')

                edge_connects_ij_bools = []
                for u, v in adjacent_edges:
                    b_edge = self._model.NewBoolVar(f'edge_{u.r}{u.c}_{v.r}{v.c}_connects_{i}{j}')

                    b_ui = self._model.NewBoolVar(f'b_{u.r}{u.c}=={i}')
                    self._model.Add(self._grid_ortools[u] == i).OnlyEnforceIf(b_ui)
                    self._model.Add(self._grid_ortools[u] != i).OnlyEnforceIf(b_ui.Not())

                    b_vj = self._model.NewBoolVar(f'b_{v.r}{v.c}=={j}')
                    self._model.Add(self._grid_ortools[v] == j).OnlyEnforceIf(b_vj)
                    self._model.Add(self._grid_ortools[v] != j).OnlyEnforceIf(b_vj.Not())

                    b_uj = self._model.NewBoolVar(f'b_{u.r}{u.c}=={j}')
                    self._model.Add(self._grid_ortools[u] == j).OnlyEnforceIf(b_uj)
                    self._model.Add(self._grid_ortools[u] != j).OnlyEnforceIf(b_uj.Not())

                    b_vi = self._model.NewBoolVar(f'b_{v.r}{v.c}=={i}')
                    self._model.Add(self._grid_ortools[v] == i).OnlyEnforceIf(b_vi)
                    self._model.Add(self._grid_ortools[v] != i).OnlyEnforceIf(b_vi.Not())

                    b_term1 = self._model.NewBoolVar(f'b_term1_{u.r}{u.c}_{v.r}{v.c}_{i}{j}')
                    self._model.AddImplication(b_term1, b_ui)
                    self._model.AddImplication(b_term1, b_vj)
                    self._model.AddBoolOr([b_ui.Not(), b_vj.Not(), b_term1])

                    b_term2 = self._model.NewBoolVar(f'b_term2_{u.r}{u.c}_{v.r}{v.c}_{i}{j}')
                    self._model.AddImplication(b_term2, b_uj)
                    self._model.AddImplication(b_term2, b_vi)
                    self._model.AddBoolOr([b_uj.Not(), b_vi.Not(), b_term2])

                    self._model.AddImplication(b_term1, b_edge)
                    self._model.AddImplication(b_term2, b_edge)
                    self._model.AddBoolOr([b_term1, b_term2, b_edge.Not()])

                    edge_connects_ij_bools.append(b_edge)

                if edge_connects_ij_bools:
                    self._model.AddBoolOr(edge_connects_ij_bools).OnlyEnforceIf(adj_bool)
                    for b in edge_connects_ij_bools:
                        self._model.AddImplication(b, adj_bool)
                else:
                    self._model.Add(adj_bool == 0)

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
            self._model.Add(sum(terms) == clue_value)
