from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class DoppelblockSolver(GameSolver):
    empty = None
    black_value = 0  # must stay 0

    def __init__(self, grid: Grid, row_sums_clues: list, column_sums_clues: list):
        self._grid = grid
        if self._grid.rows_number != self._grid.columns_number:
            raise ValueError("The grid must be square")
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        self._row_sums_clues = row_sums_clues
        self._column_sums_clues = column_sums_clues
        self._model = cp_model.CpModel()
        self._grid_vars: Grid | None = None
        self._is_black_bools_rows: list[list[cp_model.IntVar]] | None = None
        self._is_black_bools_cols: list[list[cp_model.IntVar]] | None = None
        self._previous_solution: Grid | None = None

    def get_solution(self) -> Grid:
        n = self.rows_number
        self._grid_vars = Grid([[self._model.NewIntVar(0, n - 2, f"cell_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
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

    def _compute_solution(self):
        solver = cp_model.CpSolver()
        status = solver.Solve(self._model)
        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return Grid.empty()
        grid = Grid([[solver.Value(self._grid_vars[Position(i, j)]) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def _add_constrains(self):
        self._add_initials_constraints()
        self._add_two_black_cells_and_distincts_numbers_constraints()
        self._add_sums_clues_constraints()

    def _add_initials_constraints(self):
        for position, value in self._grid:
            if value != self.empty:
                self._model.Add(self._grid_vars[position] == value)

    def _add_two_black_cells_and_distincts_numbers_constraints(self):
        n = self.rows_number
        max_num = n - 2

        is_black_row = [[self._model.NewBoolVar(f"is_black_r{r}_c{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
        is_black_col = [[is_black_row[r][c] for r in range(self.rows_number)] for c in range(self.columns_number)]

        for r in range(self.rows_number):
            for c in range(self.columns_number):
                v = self._grid_vars[Position(r, c)]
                b = is_black_row[r][c]
                self._model.Add(v == self.black_value).OnlyEnforceIf(b)
                self._model.Add(v != self.black_value).OnlyEnforceIf(b.Not())

        for r in range(self.rows_number):
            self._model.Add(sum(is_black_row[r][c] for c in range(self.columns_number)) == 2)
        for c in range(self.columns_number):
            self._model.Add(sum(is_black_col[c][r] for r in range(self.rows_number)) == 2)

        for r in range(self.rows_number):
            transformed = []
            for c in range(self.columns_number):
                v = self._grid_vars[Position(r, c)]
                b = is_black_row[r][c]
                t = self._model.NewIntVar(-self.columns_number, max_num, f"t_row_{r}_{c}")
                neg_const = -c - 1
                self._model.Add(t == neg_const).OnlyEnforceIf(b)
                self._model.Add(t == v).OnlyEnforceIf(b.Not())
                transformed.append(t)
            self._model.AddAllDifferent(transformed)

        for c in range(self.columns_number):
            transformed = []
            for r in range(self.rows_number):
                v = self._grid_vars[Position(r, c)]
                b = is_black_col[c][r]
                t = self._model.NewIntVar(-self.rows_number, max_num, f"t_col_{c}_{r}")
                neg_const = -r - 1
                self._model.Add(t == neg_const).OnlyEnforceIf(b)
                self._model.Add(t == v).OnlyEnforceIf(b.Not())
                transformed.append(t)
            self._model.AddAllDifferent(transformed)

        self._is_black_bools_rows = is_black_row
        self._is_black_bools_cols = is_black_col

    def _add_sums_clues_constraints(self):
        for r, clue in enumerate(self._row_sums_clues):
            if clue != self.empty:
                line_vars = [self._grid_vars[Position(r, c)] for c in range(self.columns_number)]
                is_black = self._is_black_bools_rows[r]
                self._add_sum_for_line_constraint(line_vars, is_black, clue, "row", r)

        for c, clue in enumerate(self._column_sums_clues):
            if clue != self.empty:
                line_vars = [self._grid_vars[Position(r, c)] for r in range(self.rows_number)]
                is_black = [self._is_black_bools_cols[c][r] for r in range(self.rows_number)]
                self._add_sum_for_line_constraint(line_vars, is_black, clue, "col", c)

    def _add_sum_for_line_constraint(self, line_vars: list, is_black_bools: list, clue: int, axis: str, index: int):
        # Pair-based formulation: for each i<j, if both endpoints are black, sum elements strictly between them.
        length = len(line_vars)
        max_between_sum = (self.rows_number - 2) * (self.rows_number - 1) // 2  # safe bound
        sum_vars = []
        for i in range(length):
            for j in range(i + 1, length):
                bi = is_black_bools[i]
                bj = is_black_bools[j]
                pair_black = self._model.NewBoolVar(f"pair_{axis}{index}_{i}_{j}")
                # Enforce pair == (bi AND bj) using linear constraints on Booleans
                self._model.Add(pair_black <= bi)
                self._model.Add(pair_black <= bj)
                self._model.Add(pair_black >= bi + bj - 1)

                between = [line_vars[k] for k in range(i + 1, j)]
                s = self._model.NewIntVar(0, max_between_sum, f"between_{axis}{index}_{i}_{j}")
                if between:
                    self._model.Add(sum(between) == s).OnlyEnforceIf(pair_black)
                else:
                    self._model.Add(s == 0).OnlyEnforceIf(pair_black)
                self._model.Add(s == 0).OnlyEnforceIf(pair_black.Not())
                sum_vars.append(s)

        if sum_vars:
            self._model.Add(sum(sum_vars) == clue)
        else:
            self._model.Add(clue == 0)
