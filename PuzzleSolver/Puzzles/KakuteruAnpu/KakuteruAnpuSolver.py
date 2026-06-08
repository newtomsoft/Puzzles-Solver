from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class KakuteruAnpuSolver(GameSolver):
    def __init__(self, numbers_grid: Grid, regions_grid: Grid):
        super().__init__()
        self._numbers_grid = numbers_grid
        self._regions_grid = regions_grid
        self._regions = self._regions_grid.get_regions()
        self.rows_number = self._numbers_grid.rows_number
        self.columns_number = self._numbers_grid.columns_number
        self._model = cp_model.CpModel()
        self._grid_vars: Grid | None = None
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_vars = Grid([[self._model.new_bool_var(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._grid_vars is None:
            self._init_solver()

        status = self._solver.solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        solution = Grid([[self._solver.boolean_value(self._grid_vars.value(i, j)) for j in range(self.columns_number)] for i in range(self.rows_number)])
        self._previous_solution = solution
        return solution

    def get_other_solution(self):
        if self._previous_solution is None:
            return self.get_solution()

        terms = [self._grid_vars[position] for position, value in self._previous_solution if not value]
        self._model.add_bool_or(terms)

        return self.get_solution()

    def _add_constraints(self):
        self._add_black_regions_constraints()
        self._add_no_black_neighbors_between_regions_constraints()
        self._add_global_black_diagonal_connectivity_constraint()

    def _add_black_regions_constraints(self):
        for region in self._regions.values():
            self._add_black_region_constraint(region)

    def _add_black_region_constraint(self, region: frozenset[Position]):
        self._add_region_connectivity_constraint(region)
        number = max(0 if (number := self._numbers_grid[position]) is None else number for position in region)
        if number != 0:
            self._model.add(sum([self._grid_vars[position] for position in region]) == number)

    def _add_region_connectivity_constraint(self, region: frozenset[Position]):
        region_list = list(region)
        total_cells = len(region_list)
        if total_cells <= 1:
            return

        rank_vars = {}
        is_root_vars = {}
        for pos in region_list:
            rank_vars[pos] = self._model.new_int_var(0, total_cells - 1, f"rank_reg_{pos.r}_{pos.c}")
            is_root_vars[pos] = self._model.new_bool_var(f"root_reg_{pos.r}_{pos.c}")

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
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = Position(pos.r + dx, pos.c + dy)
                if neighbor in rank_vars:
                    parent = self._model.new_bool_var(f"parent_reg_{pos.r}_{pos.c}_{neighbor.r}_{neighbor.c}")
                    self._model.add(self._grid_vars[neighbor] == 1).OnlyEnforceIf(parent)
                    self._model.add(rank_vars[neighbor] < rank_vars[pos]).OnlyEnforceIf(parent)
                    parent_literals.append(parent)
            if parent_literals:
                self._model.add_bool_or(parent_literals).OnlyEnforceIf([is_black, is_root.negated(), region_has_black])

    def _add_global_black_diagonal_connectivity_constraint(self):
        total_cells = self.rows_number * self.columns_number
        self._rank_vars = Grid([[self._model.new_int_var(0, total_cells - 1, f"rank_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        is_root_vars = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                is_root = self._model.new_bool_var(f"is_root_{r}_{c}")
                is_root_vars.append(is_root)
                is_black = self._grid_vars[pos]
                self._model.add(is_root <= is_black)
                self._model.add(self._rank_vars[pos] == 0).OnlyEnforceIf(is_root)
        self._model.add(sum(is_root_vars) == 1)
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                is_black = self._grid_vars[pos]
                is_root = is_root_vars[r * self.columns_number + c]
                parent_literals = []
                for neighbor in self._grid_vars.neighbors_positions(pos, mode='diagonal'):
                    parent = self._model.new_bool_var(f"parent_{r}_{c}_{neighbor.r}_{neighbor.c}")
                    self._model.add(self._grid_vars[neighbor] == 1).OnlyEnforceIf(parent)
                    self._model.add(self._rank_vars[neighbor] < self._rank_vars[pos]).OnlyEnforceIf(parent)
                    parent_literals.append(parent)
                if parent_literals:
                    self._model.add_bool_or(parent_literals).OnlyEnforceIf([is_black, is_root.negated()])

    def _add_no_black_neighbors_between_regions_constraints(self):
        for region in self._regions.values():
            self._add_no_black_neighbors_region_constraint(region)

    def _add_no_black_neighbors_region_constraint(self, region: frozenset[Position]):
        region_set = set(region)
        for position in region:
            for neighbor in self._numbers_grid.neighbors_positions(position):
                if neighbor not in region_set:
                    self._model.add_bool_or([self._grid_vars[position].negated(), self._grid_vars[neighbor].negated()])

