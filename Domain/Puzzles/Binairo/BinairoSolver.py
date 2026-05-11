from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class BinairoSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 4 or self.columns_number < 4:
            raise ValueError("Binairo grid must be at least 4x4")
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars = Grid.empty()
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        self._grid_vars = Grid([[self._model.new_bool_var(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

        status = self._solver.solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None or self._previous_solution.is_empty():
            return Grid.empty()

        vars_to_block = []
        for position, value in self._previous_solution:
            var = self._grid_vars[position]
            if value == 1:
                vars_to_block.append(var.negated())
            else:
                vars_to_block.append(var)
        self._model.add_bool_or(vars_to_block)

        status = self._solver.solve(self._model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        return Grid([[self._solver.boolean_value(self._grid_vars[r][c]) for c in range(self.columns_number)] for r in range(self.rows_number)])

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_half_true_false_by_line_constraints()
        self._add_unique_line_constraints()
        self._add_not_same_3_adjacent_constraints()

    def _add_initial_constraints(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._grid.value(r, c) == 0:
                    self._model.add(self._grid_vars[r][c] == 0)
                elif self._grid.value(r, c) == 1:
                    self._model.add(self._grid_vars[r][c] == 1)

    def _add_half_true_false_by_line_constraints(self):
        target_per_row = (self.columns_number + 1) // 2
        target_per_col = (self.rows_number + 1) // 2
        for r in range(self.rows_number):
            self._model.add(sum(self._grid_vars[r][c] for c in range(self.columns_number)) == target_per_row)
        for c in range(self.columns_number):
            self._model.add(sum(self._grid_vars[r][c] for r in range(self.rows_number)) == target_per_col)

    def _add_unique_line_constraints(self):
        for r0 in range(1, self.rows_number):
            for r1 in range(r0):
                diff_vars = []
                for c in range(self.columns_number):
                    diff = self._model.new_bool_var(f"diff_row_{r0}_{r1}_c{c}")
                    self._model.add(self._grid_vars[r0][c] != self._grid_vars[r1][c]).only_enforce_if(diff)
                    self._model.add(self._grid_vars[r0][c] == self._grid_vars[r1][c]).only_enforce_if(diff.negated())
                    diff_vars.append(diff)
                self._model.add_bool_or(diff_vars)
        for c0 in range(1, self.columns_number):
            for c1 in range(c0):
                diff_vars = []
                for r in range(self.rows_number):
                    diff = self._model.new_bool_var(f"diff_col_{c0}_{c1}_r{r}")
                    self._model.add(self._grid_vars[r][c0] != self._grid_vars[r][c1]).only_enforce_if(diff)
                    self._model.add(self._grid_vars[r][c0] == self._grid_vars[r][c1]).only_enforce_if(diff.negated())
                    diff_vars.append(diff)
                self._model.add_bool_or(diff_vars)

    def _add_not_same_3_adjacent_constraints(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number - 2):
                self._model.add_linear_constraint(
                    sum(self._grid_vars[r][c + i] for i in range(3)), 1, 2
                )
        for c in range(self.columns_number):
            for r in range(self.rows_number - 2):
                self._model.add_linear_constraint(
                    sum(self._grid_vars[r + i][c] for i in range(3)), 1, 2
                )
