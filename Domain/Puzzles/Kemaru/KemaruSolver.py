from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Ports.SolverEngine import SolverEngine
from Domain.Puzzles.GameSolver import GameSolver


class KemaruSolver(GameSolver):
    def __init__(self, grid: Grid, region_grid:Grid, solver_engine: SolverEngine):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._region_grid = region_grid
        self._regions = self._region_grid.get_regions()
        if len(self._regions) < 2:
            raise ValueError("The grid must have at least 2 regions")
        self._solver = solver_engine
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[self._solver.int(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constrains()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        self._solver.add(self._solver.Not(self._solver.And([self._grid_z3[position] == value for position, value in self._previous_solution])))
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self):
        if not self._solver.has_solution():
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[self._solver.eval(model.eval(self._grid_z3[Position(i, j)])) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def _add_constrains(self):
        self._add_initial_constraints()
        self._add_regions_distinct_and_max_value_constraints()

    def _add_initial_constraints(self):
        for grid_z3_value, number_value in [(self._grid_z3[position],number_value) for position, number_value in self._grid]:
            if number_value > 0:
                self._solver.add(grid_z3_value == number_value)
            else:
                self._solver.add(grid_z3_value >= 1)

    def _add_regions_distinct_and_max_value_constraints(self):
        for region_positions in self._regions.values():
            self._solver.add(self._solver.distinct([self._grid_z3[position] for position in region_positions]))
            for position in region_positions:
                self._add_max_value_constraints(position, len(region_positions))
                self._add_neighbors_not_same_value_constraint(position)

    def _add_max_value_constraints(self, position, region_positions_len: int):
        self._solver.add(self._grid_z3[position] <= region_positions_len)

    def _add_neighbors_not_same_value_constraint(self, position):
        self._solver.add(self._solver.And([self._grid_z3[neighbor_position] != self._grid_z3[position] for neighbor_position in self._grid.neighbors_positions(position, 'all')]))
