from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class HakoiriSolver(GameSolver):
    def __init__(self, region_grid: Grid[int], value_grid: Grid[int]):
        super().__init__()
        self._region_grid = region_grid
        self._value_grid = value_grid
        self.rows_number = self._region_grid.rows_number
        self.columns_number = self._region_grid.columns_number
        self._model = cp_model.CpModel()
        self._grid_vars: Grid | None = None
        self._is_filled: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        if self._grid_vars is None:
            self._init_solver()

        status = self._solver.solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        solution = self._build_solution()
        self._previous_solution = solution
        return solution

    def _init_solver(self):
        self._grid_vars = Grid([[self._model.new_int_var(0, 3, f"cell_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._is_filled = Grid([[self._model.new_bool_var(f"is_filled_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def _build_solution(self) -> Grid:
        return Grid([[self._solver.value(self._grid_vars.value(i, j)) for j in range(self.columns_number)] for i in range(self.rows_number)])

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()

        diffs = []
        for position, val in self._previous_solution:
            if val == 0:
                continue
            diff = self._model.new_bool_var(f"diff_{position.r}_{position.c}")
            self._model.add(self._grid_vars[position] != val).OnlyEnforceIf(diff)
            self._model.add(self._grid_vars[position] == val).OnlyEnforceIf(diff.negated())
            diffs.append(diff)

        if diffs:
            self._model.add_bool_or(diffs)

        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_no_equal_neighbors_constraints()
        self._add_each_value_one_time_in_regions_constraints()
        self._add_filled_connectivity_constraint()

    def _add_initial_constraints(self):
        for position, value in self._value_grid:
            if value > 0:
                self._model.add(self._grid_vars[position] == value)
            else:
                self._model.add(self._grid_vars[position] >= 0)
                self._model.add(self._grid_vars[position] <= 3)

        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                self._model.add(self._grid_vars[pos] > 0).OnlyEnforceIf(self._is_filled[pos])
                self._model.add(self._grid_vars[pos] == 0).OnlyEnforceIf(self._is_filled[pos].negated())

    def _add_no_equal_neighbors_constraints(self):
        for position, value in self._grid_vars:
            neighbors_positions = self._grid_vars.neighbors_positions(position, 'diagonal')
            for neighbor in neighbors_positions:
                self._model.add(self._grid_vars[neighbor] != value).OnlyEnforceIf(self._is_filled[position])

    def _add_each_value_one_time_in_regions_constraints(self):
        positions_by_region = self._region_grid.get_regions()
        for region, positions in positions_by_region.items():
            for value in range(1, 4):
                is_value_vars = []
                for position in positions:
                    is_val = self._model.new_bool_var(f"is_{value}_r{region}_{position.r}_{position.c}")
                    self._model.add(self._grid_vars[position] == value).OnlyEnforceIf(is_val)
                    self._model.add(self._grid_vars[position] != value).OnlyEnforceIf(is_val.negated())
                    is_value_vars.append(is_val)
                self._model.add(sum(is_value_vars) == 1)

    def _add_filled_connectivity_constraint(self):
        total_cells = self.rows_number * self.columns_number
        self._rank_vars = Grid([[self._model.new_int_var(0, total_cells - 1, f"rank_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        is_root_vars = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                is_root = self._model.new_bool_var(f"is_root_{r}_{c}")
                is_root_vars.append(is_root)
                self._model.add(is_root <= self._is_filled[pos])
                self._model.add(self._rank_vars[pos] == 0).OnlyEnforceIf(is_root)
        self._model.add(sum(is_root_vars) == 1)
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                is_root = is_root_vars[r * self.columns_number + c]
                parent_literals = []
                for neighbor in self._grid_vars.neighbors_positions(pos):
                    parent = self._model.new_bool_var(f"parent_{r}_{c}_{neighbor.r}_{neighbor.c}")
                    self._model.add(self._is_filled[neighbor] == 1).OnlyEnforceIf(parent)
                    self._model.add(self._rank_vars[neighbor] < self._rank_vars[pos]).OnlyEnforceIf(parent)
                    parent_literals.append(parent)
                if parent_literals:
                    self._model.add_bool_or(parent_literals).OnlyEnforceIf([self._is_filled[pos], is_root.negated()])
