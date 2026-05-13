from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class HeyablockSolver(GameSolver):
    def __init__(self, grid: Grid, region_grid: Grid):
        self._grid = grid
        self._region_grid = region_grid
        self._rows = grid.rows_number
        self._cols = grid.columns_number
        self._regions = region_grid.get_regions()
        if len(self._regions) < 2:
            raise ValueError("The grid must have at least 2 regions")
        self._region_number_map = self._build_region_number_map()
        self._solver = cp_model.CpSolver()
        self._model = None
        self._grid_vars = None
        self._previous_solution = None

    def _build_region_number_map(self) -> dict[int, int | None]:
        region_number_map = {}
        for region_id, positions in self._regions.items():
            number = None
            for pos in positions:
                val = self._grid[pos]
                if val is not None and isinstance(val, int):
                    number = val
                    break
            region_number_map[region_id] = number
        return region_number_map

    def _init_solver(self):
        self._model = cp_model.CpModel()
        self._grid_vars = Grid([[self._model.new_bool_var(f"grid_{r}_{c}") for c in range(self._cols)] for r in range(self._rows)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._grid_vars is None:
            self._init_solver()

        status = self._solver.solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        self._previous_solution = self._build_solution_grid()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()

        previous_black_cells = [pos for pos, val in self._previous_solution if not val]
        if previous_black_cells:
            self._model.add_bool_or([self._grid_vars[p].negated() for p in previous_black_cells])

        status = self._solver.solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        self._previous_solution = self._build_solution_grid()
        return self._previous_solution

    def _build_solution_grid(self) -> Grid:
        return Grid([[1 - self._solver.value(self._grid_vars[r][c]) for c in range(self._cols)] for r in range(self._rows)])

    def _add_constraints(self):
        self._add_region_count_constraints()
        self._add_cross_boundary_constraints()
        self._add_white_segment_not_crossing_more_1_boundary_constraints()
        self._add_white_connectivity_constraint()
        self._add_region_black_connectivity_constraints()

    def _add_white_connectivity_constraint(self):
        total_cells = self._rows * self._cols
        self._rank_vars = Grid([[self._model.new_int_var(0, total_cells - 1, f"rank_{r}_{c}") for c in range(self._cols)] for r in range(self._rows)])
        is_root_vars = []
        for r in range(self._rows):
            for c in range(self._cols):
                pos = Position(r, c)
                is_root = self._model.new_bool_var(f"is_root_{r}_{c}")
                is_root_vars.append(is_root)
                is_white = self._grid_vars[pos].negated()
                self._model.add(is_root <= is_white)
                self._model.add(self._rank_vars[pos] == 0).OnlyEnforceIf(is_root)
        self._model.add(sum(is_root_vars) == 1)
        for r in range(self._rows):
            for c in range(self._cols):
                pos = Position(r, c)
                is_white = self._grid_vars[pos].negated()
                is_root = is_root_vars[r * self._cols + c]
                parent_literals = []
                for neighbor in self._grid_vars.neighbors_positions(pos):
                    parent = self._model.new_bool_var(f"parent_{r}_{c}_{neighbor.r}_{neighbor.c}")
                    self._model.add(self._grid_vars[neighbor] == 0).OnlyEnforceIf(parent)
                    self._model.add(self._rank_vars[neighbor] < self._rank_vars[pos]).OnlyEnforceIf(parent)
                    parent_literals.append(parent)
                if parent_literals:
                    self._model.add_bool_or(parent_literals).OnlyEnforceIf([is_white, is_root.negated()])

    def _add_region_black_connectivity_constraints(self):
        for region in self._regions.values():
            self._add_region_black_connectivity_constraint(region)

    def _add_region_black_connectivity_constraint(self, region: frozenset[Position]):
        region_list = list(region)
        region_size = len(region_list)
        if region_size <= 1:
            return

        rank_vars = {}
        is_root_vars = {}
        for pos in region_list:
            rank_vars[pos] = self._model.new_int_var(0, region_size - 1, f"rank_region_{pos.r}_{pos.c}")
            is_root_vars[pos] = self._model.new_bool_var(f"root_region_{pos.r}_{pos.c}")

        region_has_black = self._model.new_bool_var(f"region_has_black_{region_list[0].r}_{region_list[0].c}")
        region_sum = sum(self._grid_vars[pos] for pos in region_list)
        self._model.add(region_sum >= 1).OnlyEnforceIf(region_has_black)
        self._model.add(region_sum == 0).OnlyEnforceIf(region_has_black.negated())

        self._model.add(sum(is_root_vars[pos] for pos in region_list) == 1).OnlyEnforceIf(region_has_black)
        self._model.add(sum(is_root_vars[pos] for pos in region_list) == 0).OnlyEnforceIf(region_has_black.negated())

        for pos in region_list:
            is_black = self._grid_vars[pos]
            self._model.add(is_root_vars[pos] <= is_black)
            self._model.add(is_root_vars[pos] <= region_has_black)
            self._model.add(rank_vars[pos] == 0).OnlyEnforceIf(is_root_vars[pos])

        for pos in region_list:
            is_black = self._grid_vars[pos]
            is_root = is_root_vars[pos]
            parent_literals = []
            for neighbor in self._grid_vars.neighbors_positions(pos):
                if neighbor in rank_vars:
                    parent = self._model.new_bool_var(f"parent_region_{pos.r}_{pos.c}_{neighbor.r}_{neighbor.c}")
                    self._model.add(self._grid_vars[neighbor] == 1).OnlyEnforceIf(parent)
                    self._model.add(rank_vars[neighbor] < rank_vars[pos]).OnlyEnforceIf(parent)
                    parent_literals.append(parent)
            if parent_literals:
                self._model.add_bool_or(parent_literals).OnlyEnforceIf([is_black, is_root.negated(), region_has_black])

    def _add_region_count_constraints(self):
        for region_id, positions in self._regions.items():
            number = self._region_number_map[region_id]
            black_count = sum(self._grid_vars[p] for p in positions)
            if number is not None:
                self._model.add(black_count == number)
            else:
                self._model.add(black_count >= 1)

    def _add_cross_boundary_constraints(self):
        for position, _ in self._grid:
            region_id = self._region_grid[position]
            for neighbor in self._grid.neighbors_positions(position):
                neighbor_region_id = self._region_grid[neighbor]
                if region_id != neighbor_region_id:
                    self._model.add(self._grid_vars[position] + self._grid_vars[neighbor] <= 1)

    def _add_white_segment_not_crossing_more_1_boundary_constraints(self):
        for row in range(self._grid.rows_number):
            positions = [Position(row, column) for column in range(self._grid.columns_number)]
            self._add_white_segment_not_crossing_more_1_boundary_in_position_constraints(positions)
        for column in range(self._grid.columns_number):
            positions = [Position(row, column) for row in range(self._grid.rows_number)]
            self._add_white_segment_not_crossing_more_1_boundary_in_position_constraints(positions)

    def _add_white_segment_not_crossing_more_1_boundary_in_position_constraints(self, positions: list[Position]):
        groups = []
        current_region = None
        current_group = []
        for position in positions:
            region_id = 0
            for current_region_id, region_positions in self._regions.items():
                if position in region_positions:
                    region_id = current_region_id
                    break
            if region_id != current_region:
                if current_group:
                    groups.append((current_region, current_group))
                current_region = region_id
                current_group = [position]
            else:
                current_group.append(position)
        if current_group:
            groups.append((current_region, current_group))
        if len(groups) <= 2:
            return
        for i in range(1, len(groups) - 1):
            prev_group = groups[i - 1][1]
            mid_group = groups[i][1]
            next_group = groups[i + 1][1]
            mid_vars = [self._grid_vars[p] for p in mid_group]
            adj_vars = [self._grid_vars[prev_group[-1]], self._grid_vars[next_group[0]]]
            self._model.add_bool_or(mid_vars + adj_vars)