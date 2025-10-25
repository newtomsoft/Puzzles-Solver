from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver

_ = 0


class From1ToXSolver(GameSolver):
    def __init__(self, grid: Grid, region_grid: Grid, rows_clues: list, columns_clues: list):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._rows_clues = rows_clues
        self._columns_clues = columns_clues
        self._region_grid = region_grid
        self._regions = self._region_grid.get_regions()
        if len(self._regions) < 2:
            raise ValueError("The grid must have at least 2 regions")
        self._model = cp_model.CpModel()
        self._grid_vars: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        max_region_size = max(len(region_positions) for region_positions in self._regions.values())
        self._grid_vars = Grid([[self._model.NewIntVar(1, max_region_size, f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constrains()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()
        if self._previous_solution.is_empty():
            return Grid.empty()

        bool_vars = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                prev_val = self._previous_solution.value(r, c)
                diff = self._model.NewBoolVar(f"diff_r{r}_c{c}")
                self._model.Add(self._grid_vars[Position(r, c)] != prev_val).OnlyEnforceIf(diff)
                self._model.Add(self._grid_vars[Position(r, c)] == prev_val).OnlyEnforceIf(diff.Not())
                bool_vars.append(diff)
        self._model.AddBoolOr(bool_vars)

        return self._compute_solution()

    def _compute_solution(self) -> Grid:
        solver = cp_model.CpSolver()
        status = solver.Solve(self._model)
        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return Grid.empty()
        grid = Grid([[solver.Value(self._grid_vars[Position(i, j)]) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def _add_constrains(self):
        self._add_initial_constraints()
        self._add_regions_distinct_and_max_value_constraints()
        self._add_clues_constraints()

    def _add_initial_constraints(self):
        for position, number_value in self._grid:
            if number_value != _:
                self._model.Add(self._grid_vars[position] == number_value)
            else:
                self._model.Add(self._grid_vars[position] >= 1)

    def _add_regions_distinct_and_max_value_constraints(self):
        for region_positions in self._regions.values():
            region_size = len(region_positions)
            self._model.AddAllDifferent([self._grid_vars[position] for position in region_positions])
            for position in region_positions:
                self._add_max_value_constraints(position, region_size)
                self._add_neighbors_not_same_value_constraint(position)

    def _add_max_value_constraints(self, position, region_positions_len: int):
        self._model.Add(self._grid_vars[position] <= region_positions_len)

    def _add_neighbors_not_same_value_constraint(self, position):
        for neighbor_position in self._grid.neighbors_positions(position, 'orthogonal'):
            self._model.Add(self._grid_vars[neighbor_position] != self._grid_vars[position])

    def _add_clues_constraints(self):
        for r in range(self.rows_number):
            if self._rows_clues[r] != _:
                self._model.Add(sum(self._grid_vars[Position(r, c)] for c in range(self.columns_number)) == self._rows_clues[r])

        for c in range(self.columns_number):
            if self._columns_clues[c] != _:
                self._model.Add(sum(self._grid_vars[Position(r, c)] for r in range(self.rows_number)) == self._columns_clues[c])
