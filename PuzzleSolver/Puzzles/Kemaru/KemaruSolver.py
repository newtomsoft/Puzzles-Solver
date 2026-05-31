from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class KemaruSolver(GameSolver):
    def __init__(self, grid: Grid, region_grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._region_grid = region_grid
        self._regions = self._region_grid.get_regions()
        if len(self._regions) < 2:
            raise ValueError("The grid must have at least 2 regions")
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        max_region_size = max(len(p) for p in self._regions.values())
        self._grid_z3 = Grid([[self._model.new_int_var(1, max_region_size, f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constrains()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        eq_vars = []
        for position, value in self._previous_solution:
            b = self._model.new_bool_var(f"block_{position.r}_{position.c}")
            self._model.Add(self._grid_z3[position] == value).OnlyEnforceIf(b)
            self._model.Add(self._grid_z3[position] != value).OnlyEnforceIf(b.Not())
            eq_vars.append(b)
        self._model.Add(sum(eq_vars) <= len(eq_vars) - 1)
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self):
        status = self._solver.Solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()
        grid = Grid([[self._solver.Value(self._grid_z3[Position(i, j)]) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def _add_constrains(self):
        self._add_initial_constraints()
        self._add_regions_distinct_and_max_value_constraints()

    def _add_initial_constraints(self):
        for grid_z3_value, number_value in [(self._grid_z3[position], number_value) for position, number_value in self._grid]:
            if number_value > 0:
                self._model.Add(grid_z3_value == number_value)
            else:
                self._model.Add(grid_z3_value >= 1)

    def _add_regions_distinct_and_max_value_constraints(self):
        for region_positions in self._regions.values():
            self._model.AddAllDifferent([self._grid_z3[position] for position in region_positions])
            for position in region_positions:
                self._add_max_value_constraints(position, len(region_positions))
                self._add_neighbors_not_same_value_constraint(position)

    def _add_max_value_constraints(self, position, region_positions_len: int):
        self._model.Add(self._grid_z3[position] <= region_positions_len)

    def _add_neighbors_not_same_value_constraint(self, position):
        for neighbor_position in self._grid.neighbors_positions(position, 'all'):
            self._model.Add(self._grid_z3[neighbor_position] != self._grid_z3[position])
