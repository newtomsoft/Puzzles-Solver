from z3 import Solver, Not, And, unsat, Implies, Int

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class SnakeSolver(GameSolver):
    def __init__(self, grid: Grid, row_sums: list[int], column_sums: list[int]):
        self._grid = grid
        self._row_sums = row_sums
        self._column_sums = column_sums
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Int(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        self._solver.add(Not(And([self._grid_z3[position] == value for position, value in self._previous_solution])))
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        attempted_solutions_number = 1
        while True:
            if self._solver.check() == unsat:
                return Grid.empty()
            model = self._solver.model()
            attempt = Grid([[(model.eval(self._grid_z3.value(i, j))).as_long() for j in range(self.columns_number)] for i in range(self.rows_number)])
            if attempt.enlarge(value=0, top=1, left=1, bottom=1, right=1).are_all_cells_connected():
                print(f"Found solution in {attempted_solutions_number} attempts")
                return attempt
            attempted_solutions_number += 1
            if attempted_solutions_number > 1000000:
                return Grid.empty()
            self._solver.add(Not(And([self._grid_z3[position] == value for position, value in attempt])))

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_cells_row_sum_constraints()
        self._add_cells_column_sum_constraints()
        self._add_neighbors_count_constraints()

    def _add_initial_constraints(self):
        for position, value in self._grid_z3:
            self._solver.add(value >= 0)
            self._solver.add(value <= 1)
        for position in [position for position, value in self._grid if value == 1]:
            self._solver.add(self._grid_z3[position] == 1)

    def _add_cells_row_sum_constraints(self):
        for row_index, row_sum in [(row_index, row_sum) for row_index, row_sum in enumerate(self._row_sums) if row_sum >= 0]:
            self._solver.add(sum([self._grid_z3[row_index, c] for c in range(self.columns_number)]) == row_sum)

    def _add_cells_column_sum_constraints(self):
        for column_index, column_sum in [(column_index, column_sum) for column_index, column_sum in enumerate(self._column_sums) if column_sum >= 0]:
            self._solver.add(sum([self._grid_z3[r, column_index] for r in range(self.rows_number)]) == column_sum)

    def _add_neighbors_count_constraints(self):
        start_or_end_value = 1
        for position, position_value in self._grid:
            same_value_neighbors_count = sum([self._grid_z3[position] == neighbor_value for neighbor_value in self._grid_z3.neighbors_values(position)])
            if position_value == start_or_end_value:
                self._solver.add(same_value_neighbors_count == 1)
                continue
            self._solver.add(Implies(self._grid_z3[position] == 1, same_value_neighbors_count == 2))
