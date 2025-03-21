from Ports.SolverEngine import SolverEngine
from Puzzles.GameSolver import GameSolver
from Utils.Grid import Grid


class ZipSolver(GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._path_positions = set([position for position, value in self._grid if value == 0])
        self._checkpoints_positions = set([position for position, value in self._grid if value > 0])
        self._start_position = min([(self._grid[position], position) for position in self._checkpoints_positions], key=lambda x: x[0])[1]
        self._end_position = max([(self._grid[position], position) for position in self._checkpoints_positions], key=lambda x: x[0])[1]
        self._solver = solver_engine
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> (Grid, int):
        self._grid_z3 = Grid([[self._solver.int(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        self._solver.add(self._solver.Not(self._solver.And([self._grid_z3[position] == value for position, value in self._previous_solution])))
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        if not self._solver.has_solution():
            return Grid.empty()
        return Grid([[(self._solver.eval(self._grid_z3.value(i, j))) for j in range(self.columns_number)] for i in range(self.rows_number)])

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_path_neighbors_count_constraints()
        self._add_checkpoints_neighbors_count_constraints()
        self._add_end_position_neighbors_count_constraints()

    def _add_initial_constraints(self):
        for position in self._checkpoints_positions:
            self._solver.add(self._grid_z3[position] == self._grid[position])

    def _add_path_neighbors_count_constraints(self):
        for position in self._path_positions:
            neighbors_values = self._get_neighbors_values(position)
            same_value_neighbors_count = self._solver.sum([self._grid_z3[position] == neighbor_value for neighbor_value in neighbors_values])
            self._solver.add(same_value_neighbors_count == 2)

    def _add_checkpoints_neighbors_count_constraints(self):
        for position in self._checkpoints_positions - {self._end_position}:
            neighbors_values = self._get_neighbors_values(position)
            same_value_neighbors_count = self._solver.sum([self._grid_z3[position] == neighbor_value for neighbor_value in neighbors_values])
            self._solver.add(same_value_neighbors_count == 1)

    def _add_end_position_neighbors_count_constraints(self):
        neighbors_values = self._get_neighbors_values(self._end_position)
        same_value_neighbors_count = self._solver.sum([self._grid_z3[self._end_position] == neighbor_value for neighbor_value in neighbors_values])
        self._solver.add(same_value_neighbors_count == 0)

    def _get_neighbors_values(self, position):
        neighbors_positions = self._grid_z3.neighbors_positions(position)
        neighbors_values = (
                [self._grid_z3[position] for position in neighbors_positions if position not in self._checkpoints_positions] +
                [self._grid[position] for position in neighbors_positions if position in self._checkpoints_positions] +
                [self._grid[position] - 1 for position in neighbors_positions if position in self._checkpoints_positions - {self._start_position}]
        )
        return neighbors_values
