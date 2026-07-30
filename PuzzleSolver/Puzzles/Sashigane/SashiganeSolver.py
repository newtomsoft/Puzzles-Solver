from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from PuzzleSolver.Puzzles.GameSolver import GameSolver
from ortools.sat.python import cp_model


class SashiganeSolver(GameSolver):
    cell_empty = None

    def __init__(self, grid: Grid):
        super().__init__()
        self._grid = grid
        self.rows = grid.rows_number
        self.cols = grid.columns_number
        self._previous_solution: RegionsGrid | None = None
        self._model = cp_model.CpModel()

        # ── decision variables ──────────────────────────────────────────
        self._pivot_rows = Grid([
            [self._model.new_int_var(0, self.rows - 1, f'pr_{r}_{c}') for c in range(self.cols)]
            for r in range(self.rows)
        ])
        self._pivot_cols = Grid([
            [self._model.new_int_var(0, self.cols - 1, f'pc_{r}_{c}') for c in range(self.cols)]
            for r in range(self.rows)
        ])
        self._is_pivot = Grid([
            [self._model.new_bool_var(f'is_pivot_{r}_{c}') for c in range(self.cols)]
            for r in range(self.rows)
        ])

        # Cache for the (cell, potential-pivot) channel variables.
        self._assigned_to: dict[tuple[int, int, int, int], cp_model.IntVar] = {}
        self._constraints_added = False

    # ── public API ─────────────────────────────────────────────────────

    def get_solution(self) -> RegionsGrid:
        if not self._constraints_added:
            self._add_constraints()
        solution = self._solve()
        if solution.is_empty():
            self._previous_solution = RegionsGrid.empty()
            return RegionsGrid.empty()
        self._previous_solution = solution
        return solution

    def get_other_solution(self) -> RegionsGrid:
        self._add_exclusion_constraints()
        solution = self._solve()
        self._previous_solution = solution
        return solution

    # ── solving ────────────────────────────────────────────────────────

    def _solve(self) -> RegionsGrid:
        status = self._solver.solve(self._model)
        if status in {cp_model.OPTIMAL, cp_model.FEASIBLE}:
            return RegionsGrid([
                [
                    self._solver.value(self._pivot_rows.value(r, c)) * self.cols
                    + self._solver.value(self._pivot_cols.value(r, c))
                    for c in range(self.cols)
                ]
                for r in range(self.rows)
            ])
        return RegionsGrid.empty()

    # ── constraint assembly ────────────────────────────────────────────

    def _add_constraints(self):
        self._add_cross_and_pivot_constraints()
        self._add_connectivity_constraints()
        self._add_l_shape_constraints()
        self._add_clue_constraints()
        self._constraints_added = True

    # ── (1) cross + pivot self-reference ───────────────────────────────

    def _add_cross_and_pivot_constraints(self):
        for pos, _ in self._grid:
            r, c = pos.r, pos.c

            row_eq = self._model.new_bool_var(f'row_eq_{r}_{c}')
            self._model.add(self._pivot_rows.value(pos) == r).only_enforce_if(row_eq)
            self._model.add(self._pivot_rows.value(pos) != r).only_enforce_if(~row_eq)

            col_eq = self._model.new_bool_var(f'col_eq_{r}_{c}')
            self._model.add(self._pivot_cols.value(pos) == c).only_enforce_if(col_eq)
            self._model.add(self._pivot_cols.value(pos) != c).only_enforce_if(~col_eq)

            self._model.add_bool_or(row_eq, col_eq)

            self._model.add_bool_and(row_eq, col_eq).only_enforce_if(self._is_pivot.value(pos))
            self._model.add_bool_or(~row_eq, ~col_eq).only_enforce_if(~self._is_pivot.value(pos))

    # ── (2) connectivity along arms ────────────────────────────────────

    def _add_connectivity_constraints(self):
        rows, cols = self.rows, self.cols
        for pos, _ in self._grid:
            r, c = pos.r, pos.c

            if r > 0:
                beyond = self._model.new_bool_var(f'beyond_up_{r}_{c}')
                self._model.add(r > self._pivot_rows.value(pos)).only_enforce_if(beyond)
                self._model.add(r <= self._pivot_rows.value(pos)).only_enforce_if(~beyond)
                self._model.add(self._pivot_rows.value(r - 1, c) == self._pivot_rows.value(pos)).only_enforce_if(beyond)
                self._model.add(self._pivot_cols.value(r - 1, c) == self._pivot_cols.value(pos)).only_enforce_if(beyond)

            if r < rows - 1:
                beyond = self._model.new_bool_var(f'beyond_down_{r}_{c}')
                self._model.add(r < self._pivot_rows.value(pos)).only_enforce_if(beyond)
                self._model.add(r >= self._pivot_rows.value(pos)).only_enforce_if(~beyond)
                self._model.add(self._pivot_rows.value(r + 1, c) == self._pivot_rows.value(pos)).only_enforce_if(beyond)
                self._model.add(self._pivot_cols.value(r + 1, c) == self._pivot_cols.value(pos)).only_enforce_if(beyond)

            if c > 0:
                beyond = self._model.new_bool_var(f'beyond_left_{r}_{c}')
                self._model.add(c > self._pivot_cols.value(pos)).only_enforce_if(beyond)
                self._model.add(c <= self._pivot_cols.value(pos)).only_enforce_if(~beyond)
                self._model.add(self._pivot_rows.value(r, c - 1) == self._pivot_rows.value(pos)).only_enforce_if(beyond)
                self._model.add(self._pivot_cols.value(r, c - 1) == self._pivot_cols.value(pos)).only_enforce_if(beyond)

            if c < cols - 1:
                beyond = self._model.new_bool_var(f'beyond_right_{r}_{c}')
                self._model.add(c < self._pivot_cols.value(pos)).only_enforce_if(beyond)
                self._model.add(c >= self._pivot_cols.value(pos)).only_enforce_if(~beyond)
                self._model.add(self._pivot_rows.value(r, c + 1) == self._pivot_rows.value(pos)).only_enforce_if(beyond)
                self._model.add(self._pivot_cols.value(r, c + 1) == self._pivot_cols.value(pos)).only_enforce_if(beyond)

    # ── (3) L-shape  (one direction per arm, each arm ≥ 1 cell) ────────

    def _add_l_shape_constraints(self):
        rows, cols = self.rows, self.cols

        for pr in range(rows):
            for pc in range(cols):
                is_pv = self._is_pivot.value(pr, pc)

                left_vars: list[cp_model.IntVar] = []
                right_vars: list[cp_model.IntVar] = []
                up_vars: list[cp_model.IntVar] = []
                down_vars: list[cp_model.IntVar] = []

                # cells on the same row
                for c in range(cols):
                    if c == pc:
                        continue
                    a = self._get_assigned_var(pr, c, pr, pc)
                    if c < pc:
                        left_vars.append(a)
                    else:
                        right_vars.append(a)

                # cells on the same column
                for r in range(rows):
                    if r == pr:
                        continue
                    a = self._get_assigned_var(r, pc, pr, pc)
                    if r < pr:
                        up_vars.append(a)
                    else:
                        down_vars.append(a)

                # helper reification
                hl = self._model.new_bool_var(f'hl_{pr}_{pc}')
                hr = self._model.new_bool_var(f'hr_{pr}_{pc}')
                hu = self._model.new_bool_var(f'hu_{pr}_{pc}')
                hd = self._model.new_bool_var(f'hd_{pr}_{pc}')

                self._model.add(sum(left_vars) >= 1).only_enforce_if(hl)
                self._model.add(sum(left_vars) == 0).only_enforce_if(~hl)

                self._model.add(sum(right_vars) >= 1).only_enforce_if(hr)
                self._model.add(sum(right_vars) == 0).only_enforce_if(~hr)

                self._model.add(sum(up_vars) >= 1).only_enforce_if(hu)
                self._model.add(sum(up_vars) == 0).only_enforce_if(~hu)

                self._model.add(sum(down_vars) >= 1).only_enforce_if(hd)
                self._model.add(sum(down_vars) == 0).only_enforce_if(~hd)

                # at most one horizontal / one vertical direction
                self._model.add(hl + hr <= 1).only_enforce_if(is_pv)
                self._model.add(hu + hd <= 1).only_enforce_if(is_pv)

                # each arm must have ≥ 1 cell
                self._model.add(hl + hr >= 1).only_enforce_if(is_pv)
                self._model.add(hu + hd >= 1).only_enforce_if(is_pv)

                # non-pivot cells must have 0 cells assigned
                self._model.add(
                    sum(left_vars) + sum(right_vars) + sum(up_vars) + sum(down_vars) == 0
                ).only_enforce_if(~is_pv)

    # ── (4) clue constraints ───────────────────────────────────────────

    def _add_clue_constraints(self):
        for pos, val in self._grid:
            if val is None:
                continue

            r, c = pos.r, pos.c

            if isinstance(val, Direction):
                self._model.add(self._is_pivot.value(pos) == 0)
                if val == Direction.up():
                    self._model.add(self._pivot_rows.value(pos) < r)
                    self._model.add(self._pivot_cols.value(pos) == c)
                    if r < self.rows - 1:
                        self._add_different_pivot_constraint(pos, Position(r + 1, c))
                elif val == Direction.down():
                    self._model.add(self._pivot_rows.value(pos) > r)
                    self._model.add(self._pivot_cols.value(pos) == c)
                    if r > 0:
                        self._add_different_pivot_constraint(pos, Position(r - 1, c))
                elif val == Direction.left():
                    self._model.add(self._pivot_rows.value(pos) == r)
                    self._model.add(self._pivot_cols.value(pos) < c)
                    if c < self.cols - 1:
                        self._add_different_pivot_constraint(pos, Position(r, c + 1))
                elif val == Direction.right():
                    self._model.add(self._pivot_rows.value(pos) == r)
                    self._model.add(self._pivot_cols.value(pos) > c)
                    if c > 0:
                        self._add_different_pivot_constraint(pos, Position(r, c - 1))

            elif isinstance(val, int) and val >= 0:
                self._model.add(self._is_pivot.value(pos) == 1)
                self._model.add(self._pivot_rows.value(pos) == r)
                self._model.add(self._pivot_cols.value(pos) == c)

                if val > 0:
                    assigned = self._all_assigned_to(r, c)
                    self._model.add(sum(assigned) == val)

    def _add_different_pivot_constraint(self, pos: Position, opposite: Position):
        """Enforce that `opposite` does NOT share its pivot with `pos`.

        Used for arrow clues: the cell behind the arrow must belong to a
        different L (the arrow cell is at the extreme end of its arm).
        """
        r, c = pos.r, pos.c
        or_, oc = opposite.r, opposite.c

        same_row = self._model.new_bool_var(f'nsr_{or_}_{oc}_{r}_{c}')
        same_col = self._model.new_bool_var(f'nsc_{or_}_{oc}_{r}_{c}')

        self._model.add(self._pivot_rows.value(or_, oc) == self._pivot_rows.value(pos)).only_enforce_if(same_row)
        self._model.add(self._pivot_rows.value(or_, oc) != self._pivot_rows.value(pos)).only_enforce_if(~same_row)
        self._model.add(self._pivot_cols.value(or_, oc) == self._pivot_cols.value(pos)).only_enforce_if(same_col)
        self._model.add(self._pivot_cols.value(or_, oc) != self._pivot_cols.value(pos)).only_enforce_if(~same_col)

        self._model.add_bool_or(~same_row, ~same_col)

    # ── helpers ────────────────────────────────────────────────────────

    def _get_assigned_var(self, r: int, c: int, pr: int, pc: int) -> cp_model.IntVar:
        """bool variable: is cell (r,c) assigned to pivot (pr,pc) ?"""
        key = (r, c, pr, pc)
        if key not in self._assigned_to:
            var = self._model.new_bool_var(f'a_{r}_{c}_{pr}_{pc}')
            mr = self._model.new_bool_var(f'mr_{r}_{c}_{pr}_{pc}')
            mc = self._model.new_bool_var(f'mc_{r}_{c}_{pr}_{pc}')
            self._model.add(self._pivot_rows.value(r, c) == pr).only_enforce_if(mr)
            self._model.add(self._pivot_rows.value(r, c) != pr).only_enforce_if(~mr)
            self._model.add(self._pivot_cols.value(r, c) == pc).only_enforce_if(mc)
            self._model.add(self._pivot_cols.value(r, c) != pc).only_enforce_if(~mc)
            self._model.add_bool_and(mr, mc).only_enforce_if(var)
            self._model.add_bool_or(~mr, ~mc).only_enforce_if(~var)
            self._assigned_to[key] = var
        return self._assigned_to[key]

    def _all_assigned_to(self, pr: int, pc: int) -> list[cp_model.IntVar]:
        """All (cell → pivot) channel variables for a given pivot."""
        return [
            self._get_assigned_var(r, c, pr, pc)
            for r in range(self.rows)
            for c in range(self.cols)
        ]

    # ── exclusion for get_other_solution ───────────────────────────────

    def _add_exclusion_constraints(self):
        if self._previous_solution is None or self._previous_solution.is_empty():
            return
        rows, cols = self.rows, self.cols
        changes = []
        for pos, _ in self._grid:
            pid = self._model.new_int_var(0, rows * cols - 1, f'pid_{pos.r}_{pos.c}')
            self._model.add(pid == self._pivot_rows.value(pos) * cols + self._pivot_cols.value(pos))

            prev = int(self._previous_solution[pos])
            diff = self._model.new_bool_var(f'diff_{pos.r}_{pos.c}')
            self._model.add(pid == prev).only_enforce_if(~diff)
            self._model.add(pid != prev).only_enforce_if(diff)
            changes.append(diff)

        self._model.add_bool_or(changes)
