from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class SnakeSolver(GameSolver):
    def __init__(self, grid: Grid, row_sums: list[int], column_sums: list[int]):
        self._grid = grid
        self._row_sums = row_sums
        self._column_sums = column_sums
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars: Grid | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_vars = Grid([[self._model.NewIntVar(0, 1, f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None or self._previous_solution.is_empty():
            return Grid.empty()

        previous_solution_literals = []
        for position, value in self._previous_solution:
            temp_var = self._model.NewBoolVar(f"prev_{position.r}_{position.c}")
            self._model.Add(self._grid_vars[position] == value).OnlyEnforceIf(temp_var)
            self._model.Add(self._grid_vars[position] != value).OnlyEnforceIf(temp_var.Not())
            previous_solution_literals.append(temp_var)

        if previous_solution_literals:
            self._model.AddBoolOr([lit.Not() for lit in previous_solution_literals])

        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        attempted_solutions_number = 1
        max_attempts = 1000000

        while attempted_solutions_number <= max_attempts:
            status = self._solver.Solve(self._model)

            if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
                return Grid.empty()

            attempt = Grid([[self._solver.Value(self._grid_vars[i, j]) for j in range(self.columns_number)] for i in range(self.rows_number)])

            if attempt.enlarge(value=0, top=1, left=1, bottom=1, right=1).are_all_cells_connected():
                print(f"Found solution in {attempted_solutions_number} attempts")
                return attempt

            solution_literals = []
            for position, value in attempt:
                temp_var = self._model.NewBoolVar(f"attempt_{attempted_solutions_number}_{position.r}_{position.c}")
                self._model.Add(self._grid_vars[position] == value).OnlyEnforceIf(temp_var)
                self._model.Add(self._grid_vars[position] != value).OnlyEnforceIf(temp_var.Not())
                solution_literals.append(temp_var)

            if solution_literals:
                self._model.AddBoolOr([lit.Not() for lit in solution_literals])

            attempted_solutions_number += 1

        return Grid.empty()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_cells_row_sum_constraints()
        self._add_cells_column_sum_constraints()
        self._add_neighbors_count_constraints()

    def _add_initial_constraints(self):
        for position in [position for position, value in self._grid if value == 1]:
            self._model.Add(self._grid_vars[position] == 1)

    def _add_cells_row_sum_constraints(self):
        for row_index, row_sum in [(row_index, row_sum) for row_index, row_sum in enumerate(self._row_sums) if row_sum >= 0]:
            self._model.Add(sum([self._grid_vars[row_index, c] for c in range(self.columns_number)]) == row_sum)

    def _add_cells_column_sum_constraints(self):
        for column_index, column_sum in [(column_index, column_sum) for column_index, column_sum in enumerate(self._column_sums) if column_sum >= 0]:
            self._model.Add(sum([self._grid_vars[r, column_index] for r in range(self.rows_number)]) == column_sum)

    def _add_neighbors_count_constraints(self):
        start_or_end_value = 1
        for position, position_value in self._grid:
            neighbor_equality_vars = []
            for neighbor_position in self._grid.neighbors_positions(position):
                equality_var = self._model.NewBoolVar(f"eq_{position}_{neighbor_position}")
                self._model.Add(self._grid_vars[position] == self._grid_vars[neighbor_position]).OnlyEnforceIf(equality_var)
                self._model.Add(self._grid_vars[position] != self._grid_vars[neighbor_position]).OnlyEnforceIf(equality_var.Not())
                neighbor_equality_vars.append(equality_var)

            if position_value == start_or_end_value:
                self._model.Add(sum(neighbor_equality_vars) == 1)
                continue

            cell_is_one = self._model.NewBoolVar(f"cell_is_one_{position}")
            self._model.Add(self._grid_vars[position] == 1).OnlyEnforceIf(cell_is_one)
            self._model.Add(self._grid_vars[position] == 0).OnlyEnforceIf(cell_is_one.Not())

            self._model.Add(sum(neighbor_equality_vars) == 2).OnlyEnforceIf(cell_is_one)
