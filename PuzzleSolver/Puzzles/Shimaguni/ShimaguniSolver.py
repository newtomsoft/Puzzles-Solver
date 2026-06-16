from ortools.sat.python import cp_model
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.GridMask import is_outside_region, resolve_outside
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class ShimaguniSolver(GameSolver):
    def __init__(self, values_grid: Grid, regions_grid: Grid):
        super().__init__()
        self._values_grid = values_grid
        self._regions_grid = regions_grid
        self._outside = resolve_outside(values_grid)
        self._regions_positions_by_id = regions_grid.get_regions()
        self.rows_number = self._values_grid.rows_number
        self.columns_number = self._values_grid.columns_number
        
        self._model = cp_model.CpModel()
        self._grid_vars = {}
        self._region_counts = {}
        self._status = None

    def _init_model(self):
        self._create_variables()
        self._add_constraints()

    def _create_variables(self):
        for position, _ in self._values_grid:
            if (position.r, position.c) in self._outside:
                continue
            self._grid_vars[position] = self._model.new_bool_var(f'cell_{position.r}_{position.c}')

        for region_id, positions in self._regions_positions_by_id.items():
            if is_outside_region(positions, self._outside):
                continue
            region_vars = [self._grid_vars[p] for p in positions if p in self._grid_vars]
            # Constraint 1 (part A): Each region must have at least 1 black cell (or the clue count)
            rc = self._model.new_int_var(1, len(positions), f'count_region_{region_id}')
            self._model.add(rc == sum(region_vars))
            self._region_counts[region_id] = rc

    def _add_constraints(self):
        self._add_region_clue_and_connectivity_constraints()
        self._add_adjacent_regions_different_counts_constraints()
        self._add_no_cross_region_adjacency_constraints()

    def _add_region_clue_and_connectivity_constraints(self):
        """Constraint 1: Match clues and ensure connectivity within each region."""
        for region_id, positions in self._regions_positions_by_id.items():
            if is_outside_region(positions, self._outside):
                continue
            clue = self._get_region_clue(positions)
            
            if clue is not None and clue > 0:
                self._model.add(self._region_counts[region_id] == clue).WithName(f'clue_region_{region_id}')
                self._add_connectivity_constraint(positions, clue)
            else:
                # If no clue, count is already >= 1 by IntVar range
                self._add_connectivity_constraint_unknown_count(positions)

    def _get_region_clue(self, positions):
        for p in positions:
            value = self._values_grid[p]
            if value is not None and value != GameSolver.cell_outside:
                return value
        return None

    def _add_adjacent_regions_different_counts_constraints(self):
        for region_id, positions in self._regions_positions_by_id.items():
            if is_outside_region(positions, self._outside):
                continue
            adjacent_region_ids = self._get_adjacent_region_ids(region_id, positions)
            for other_id in adjacent_region_ids:
                if other_id > region_id:
                    self._model.add(self._region_counts[region_id] != self._region_counts[other_id]).WithName(f'diff_counts_{region_id}_{other_id}')

    def _get_adjacent_region_ids(self, region_id, positions):
        adjacent_region_ids = set()
        for p in positions:
            for neighbor in self._regions_grid.neighbors_positions(p):
                other_region_id = self._regions_grid[neighbor]
                if other_region_id != region_id:
                    adjacent_region_ids.add(other_region_id)
        return adjacent_region_ids

    def _add_no_cross_region_adjacency_constraints(self):
        for position, _ in self._values_grid:
            if (position.r, position.c) in self._outside:
                continue
            if position not in self._grid_vars:
                continue
            region_p = self._regions_grid[position]
            for neighbor in self._values_grid.neighbors_positions(position):
                if (neighbor.r, neighbor.c) in self._outside or neighbor not in self._grid_vars:
                    continue
                if self._regions_grid[neighbor] != region_p:
                    self._model.add(self._grid_vars[position] + self._grid_vars[neighbor] <= 1).WithName(f'no_adj_{position.r}_{position.c}_{neighbor.r}_{neighbor.c}')

    def get_solution(self) -> Grid:
        if self._model is None:
            self._init_model()

        self._status = self._solver.Solve(self._model)

        if self._status == cp_model.OPTIMAL or self._status == cp_model.FEASIBLE:
            return self._compute_solution()

        return Grid.empty()

    def get_other_solution(self) -> Grid:
        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return Grid.empty()

        # Add a constraint to exclude the current solution
        literals = []
        for position, var in self._grid_vars.items():
            if self._solver.Value(var):
                literals.append(var.Not())
            else:
                literals.append(var)
        self._model.add_bool_or(literals)

        return self.get_solution()

    def _compute_solution(self) -> Grid:
        solution_matrix = [[0 for _ in range(self.columns_number)] for _ in range(self.rows_number)]
        for position, var in self._grid_vars.items():
            solution_matrix[position.r][position.c] = self._solver.Value(var)
        return Grid(solution_matrix)

    def _add_connectivity_constraint(self, positions, count):
        if count <= 1:
            return
        
        pos_list = list(positions)
        n = len(pos_list)
        dist = [self._model.new_int_var(0, n, f'dist_{p.r}_{p.c}') for p in pos_list]
        is_root = [self._model.new_bool_var(f'root_{p.r}_{p.c}') for p in pos_list]
        
        for i, p in enumerate(pos_list):
            cell_var = self._grid_vars[p]
            self._model.add(is_root[i] <= cell_var)
            self._model.add(dist[i] == 0).OnlyEnforceIf(is_root[i])
            self._model.add(dist[i] > 0).OnlyEnforceIf([cell_var, is_root[i].Not()])
            self._model.add(dist[i] == n).OnlyEnforceIf(cell_var.Not())
        
        self._model.add(sum(is_root) == 1)

        for i, p in enumerate(pos_list):
            cell_var = self._grid_vars[p]
            neighbors_in_region_indices = [j for j, op in enumerate(pos_list) if op in self._regions_grid.neighbors_positions(p)]
            
            has_lower = self._model.new_bool_var(f'has_lower_{p.r}_{p.c}')
            conditions = []
            for j in neighbors_in_region_indices:
                cond = self._model.new_bool_var(f'cond_{i}_{j}')
                self._model.add(dist[j] == dist[i] - 1).OnlyEnforceIf(cond)
                self._model.add(self._grid_vars[pos_list[j]] == 1).OnlyEnforceIf(cond)
                conditions.append(cond)
            
            if conditions:
                self._model.add_bool_or(conditions).OnlyEnforceIf(has_lower)
                self._model.add_bool_and([c.Not() for c in conditions]).OnlyEnforceIf(has_lower.Not())
                self._model.add(has_lower == 1).OnlyEnforceIf([cell_var, is_root[i].Not()])
            else:
                self._model.add(cell_var == 0).OnlyEnforceIf(is_root[i].Not())

    def _add_connectivity_constraint_unknown_count(self, positions):
        self._add_connectivity_constraint(positions, len(positions))
