from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.LinearPathGrid import LinearPathGrid
from Domain.Puzzles.GameSolver import GameSolver


class ZipSolver(GameSolver):
    def __init__(self, grid: Grid = None):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._path_positions = set([position for position, value in self._grid if value == 0])
        self._checkpoints = {value: position for position, value in self._grid if value > 0}
        self._start_position = self._checkpoints[min(self._checkpoints.keys())]
        self._finish_position = self._checkpoints[max(self._checkpoints.keys())]
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None
        self._solver_impl = None
        self._counter = 0

    def get_solution(self) -> LinearPathGrid:
        if self._solver_impl:
            return self._solver_impl.get_solution

        self._grid_z3 = Grid([[self._model.NewIntVar(0, self.rows_number * self.columns_number, f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._grid_z3.copy_walls_from_grid(self._grid)
        self._add_constraints()
        return self._compute_solution()

    def get_other_solution(self) -> Grid:
        if self._solver_impl:
            return self._solver_impl.get_other_solution()

        self._add_blocking_constraint(self._previous_solution)
        return self._compute_solution()

    def _add_blocking_constraint(self, solution):
        bs = []
        for position, value in solution:
            b = self._model.NewBoolVar(f"block_{self._counter}")
            self._counter += 1
            self._model.Add(self._grid_z3[position] == value).OnlyEnforceIf(b)
            self._model.Add(self._grid_z3[position] != value).OnlyEnforceIf(b.Not())
            bs.append(b)
        self._model.Add(sum(bs) <= len(bs) - 1)

    def _compute_solution(self) -> LinearPathGrid:
        while self._solver.Solve(self._model) in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            grid_solution = Grid([[(self._solver.Value(self._grid_z3.value(r, c))) for c in range(self.columns_number)] for r in range(self.rows_number)])
            grid_solution.set_walls(self._grid.walls)
            linear_path_grid = LinearPathGrid.from_grid_and_checkpoints(grid_solution, self._checkpoints)
            if linear_path_grid == Grid.empty():
                self._add_blocking_constraint(grid_solution)
                continue
            self._previous_solution = grid_solution
            return linear_path_grid
        return LinearPathGrid.empty()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_finish_checkpoint_not_same_value_neighbors_constraints()
        self._add_on_checkpoints_neighbors_count_constraints()
        self._add_along_path_neighbors_count_constraints()

    def _add_initial_constraints(self):
        for position in self._checkpoints.values():
            self._model.Add(self._grid_z3[position] == self._grid[position])
        for position in self._path_positions:
            self._model.Add(self._grid_z3[position] >= self._grid[self._start_position])
            self._model.Add(self._grid_z3[position] < self._grid[self._finish_position])

    def _add_finish_checkpoint_not_same_value_neighbors_constraints(self):
        neighbors_values = self._get_neighbors_values(self._finish_position)
        finish_value = self._grid[self._finish_position]
        for neighbor_value in neighbors_values:
            if isinstance(neighbor_value, int):
                if neighbor_value == finish_value:
                    self._model.Add(0 == 1)
            else:
                self._model.Add(neighbor_value != finish_value)

    def _add_along_path_neighbors_count_constraints(self):
        for position in self._path_positions:
            neighbors_values = self._get_neighbors_values(position)
            terms = self._make_eq_terms(neighbors_values, self._grid_z3[position])
            self._model.Add(sum(terms) >= 2)

    def _add_on_checkpoints_neighbors_count_constraints(self):
        self._add_checkpoint_same_neighbors_count_constraint(self._start_position)
        self._add_checkpoint_minus_one_same_neighbors_count_constraint(self._finish_position)

        for position in set(self._checkpoints.values()) - {self._start_position, self._finish_position}:
            self._add_checkpoint_same_neighbors_count_constraint(position)
            self._add_checkpoint_minus_one_same_neighbors_count_constraint(position)

    def _add_checkpoint_same_neighbors_count_constraint(self, position):
        neighbors_values = self._get_neighbors_values(position)
        checkpoint_value = self._grid[position]
        terms = self._make_eq_terms(neighbors_values, checkpoint_value)
        self._model.Add(sum(terms) >= 1)

    def _add_checkpoint_minus_one_same_neighbors_count_constraint(self, position):
        neighbors_values = self._get_neighbors_values(position)
        previous_checkpoint_value = self._grid_z3[position] - 1
        terms = self._make_eq_terms(neighbors_values, previous_checkpoint_value)
        self._model.Add(sum(terms) >= 1)

    def _make_eq_terms(self, values, target):
        terms = []
        for v in values:
            if isinstance(v, int) and isinstance(target, int):
                terms.append(1 if v == target else 0)
            else:
                b = self._model.NewBoolVar(f"eq_{self._counter}")
                self._counter += 1
                self._model.Add(v == target).OnlyEnforceIf(b)
                self._model.Add(v != target).OnlyEnforceIf(b.Not())
                terms.append(b)
        return terms

    def _get_neighbors_values(self, position):
        neighbors_positions = self._grid_z3.neighbors_positions(position)
        neighbors_values = (
                [self._grid_z3[position] for position in neighbors_positions if position not in self._checkpoints.values()] +
                [self._grid[position] for position in neighbors_positions if position in self._checkpoints.values()] +
                [self._grid[position] - 1 for position in neighbors_positions if position in set(self._checkpoints.values()) - {self._start_position}]
        )
        return neighbors_values
