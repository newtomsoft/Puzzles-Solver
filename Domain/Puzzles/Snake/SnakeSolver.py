from Domain.Board.Grid import Grid
from Domain.Ports.SolverEngine import SolverEngine
from Domain.Puzzles.GameSolver import GameSolver


class SnakeSolver(GameSolver):
    def __init__(self, grid: Grid, row_sums: list[int], column_sums: list[int], solver_engine: SolverEngine):
        self._grid = grid
        self._row_sums = row_sums
        self._column_sums = column_sums
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
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
        self._add_cells_sum_constraints()
        self._add_neighbors_count_constraints()

    def _add_initial_constraints(self):
        for position, value in self._grid_z3:
            self._solver.add(value >= 0)
            self._solver.add(value <= 1)
        for position in [position for position, value in self._grid if value == 1]:
            self._solver.add(self._grid_z3[position] == 1)

    def _add_cells_sum_constraints(self):
        for row_index, row_sum in [(i, row_sum) for i, row_sum in enumerate(self._row_sums) if row_sum >= 0]:
            self._solver.add(self._solver.sum([self._grid_z3[row_index, c] for c in range(self.columns_number)]) == row_sum)
        for column_index, column_sum in [(i, column_sum) for i, column_sum in enumerate(self._column_sums) if column_sum >= 0]:
            self._solver.add(self._solver.sum([self._grid_z3[r, column_index] for r in range(self.rows_number)]) == column_sum)

    def _add_neighbors_count_constraints(self):
        for position, position_value in self._grid:
            same_value_neighbors_count = self._solver.sum([self._grid_z3[position] == neighbor_value for neighbor_value in self._grid_z3.neighbors_values(position)])
            if position_value == 1:
                self._solver.add(same_value_neighbors_count == 1)
                continue
            self._solver.add(self._solver.Implies(self._grid_z3[position] == 1, same_value_neighbors_count == 2))
