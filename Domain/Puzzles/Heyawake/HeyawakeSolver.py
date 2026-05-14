from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class HeyawakeSolver(GameSolver):
    def __init__(self, grid: Grid, region_grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self.regions = region_grid.get_regions()
        if len(self.regions) < 2:
            raise ValueError("The grid must have at least 2 regions")
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars: Grid | None = None
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_vars = Grid([[self._model.new_bool_var(f"grid_{r}_{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._grid_vars is None:
            self._init_solver()

        status = self._solver.solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        solution = Grid([[self._solver.boolean_value(self._grid_vars.value(i, j)) for j in range(self._grid.columns_number)] for i in range(self._grid.rows_number)])
        self._previous_solution = solution
        return solution

    def get_other_solution(self):
        if self._previous_solution is None:
            return self.get_solution()

        previous_black_positions = [position for position, value in self._previous_solution if not value]
        self._model.add_bool_or([self._grid_vars[position] for position in previous_black_positions])

        return self.get_solution()

    def _add_constraints(self):
        self._add_black_cell_count_in_regions_constraints()
        self._add_no_adjacent_black_cells_touching_constraints()
        self._add_white_segment_not_crossing_more_2_regions_constraints()
        self._add_white_connectivity_constraint()

    def _add_black_cell_count_in_regions_constraints(self):
        for region in self.regions.values():
            black_cells_count_position = min([position for position in region], key=lambda p: (p.r, p.c))
            black_cells_count = self._grid[black_cells_count_position]
            if not isinstance(black_cells_count, int) or black_cells_count < 0:
                continue
            region_vars = [self._grid_vars[position] for position in region]
            self._model.add(sum(region_vars) == len(region) - black_cells_count)

    def _add_no_adjacent_black_cells_touching_constraints(self):
        for position, _ in self._grid_vars:
            for neighbor_position in self._grid.neighbors_positions(position):
                self._model.add(self._grid_vars[position] + self._grid_vars[neighbor_position] >= 1)

    def _add_white_segment_not_crossing_more_2_regions_constraints(self):
        for row in range(self._grid.rows_number):
            positions = [Position(row, column) for column in range(self._grid.columns_number)]
            self._add_white_segment_not_crossing_more_2_regions_constraints_in_positions(positions)
        for column in range(self._grid.columns_number):
            positions = [Position(row, column) for row in range(self._grid.rows_number)]
            self._add_white_segment_not_crossing_more_2_regions_constraints_in_positions(positions)

    def _add_white_segment_not_crossing_more_2_regions_constraints_in_positions(self, positions: list[Position]):
        regions = {}
        for position in positions:
            region_id = 0
            for current_region_id, region_positions in self.regions.items():
                if position in region_positions:
                    region_id = current_region_id
                    continue
            regions.setdefault(region_id, []).append(position)
        if len(regions) <= 2:
            return
        keys_regions = list(regions.keys())
        for index_region, key_region in enumerate(keys_regions[1:-1]):
            previous_key_region = keys_regions[index_region]
            next_key_region = keys_regions[index_region + 2]
            mid_region_vars = [self._grid_vars[position] for position in regions[key_region]]
            adj_vars = [self._grid_vars[regions[previous_key_region][-1]], self._grid_vars[regions[next_key_region][0]]]
            self._model.add_bool_or([v.Not() for v in mid_region_vars] + [adj.Not() for adj in adj_vars])

    def _add_white_connectivity_constraint(self):
        total_cells = self.rows_number * self.columns_number
        self._rank_vars = Grid([[self._model.new_int_var(0, total_cells - 1, f"rank_{r}_{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])

        is_root_vars = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                is_root = self._model.new_bool_var(f"is_root_{r}_{c}")
                is_root_vars.append(is_root)

                is_white = self._grid_vars[pos]
                self._model.add(is_root <= is_white)
                self._model.add(self._rank_vars[pos] == 0).OnlyEnforceIf(is_root)

        self._model.add(sum(is_root_vars) == 1)

        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                is_white = self._grid_vars[pos]
                is_root = is_root_vars[r * self.columns_number + c]

                parent_literals = []
                for neighbor in self._grid.neighbors_positions(pos):
                    parent = self._model.new_bool_var(f"parent_{r}_{c}_{neighbor.r}_{neighbor.c}")
                    self._model.add(self._grid_vars[neighbor] == 1).OnlyEnforceIf(parent)
                    self._model.add(self._rank_vars[neighbor] < self._rank_vars[pos]).OnlyEnforceIf(parent)
                    parent_literals.append(parent)

                if parent_literals:
                    self._model.add_bool_or(parent_literals).OnlyEnforceIf([is_white, is_root.negated()])
