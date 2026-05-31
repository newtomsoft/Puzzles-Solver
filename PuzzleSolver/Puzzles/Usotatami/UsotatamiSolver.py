from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class UsotatamiSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._initial_grid = grid
        self._rows_number = grid.rows_number
        self._columns_number = grid.columns_number
        self._model = cp_model.CpModel()
        self._grid_vars: Grid | None = None
        self._previous_solution: Grid | None = None
        self._clues = self._get_clues()

    def _get_clues(self) -> list[tuple[Position, int]]:
        clues = []
        for position, value in self._initial_grid:
            if value is not None and isinstance(value, int) and value >= 0:
                clues.append((position, value))
            elif isinstance(value, str) and value.isdigit():
                clues.append((position, int(value)))
        return clues

    def get_solution(self) -> Grid:
        if self._grid_vars is None:
            self._init_solver()
        solution = self._compute_solution()
        self._previous_solution = solution
        return solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()

        if self._grid_vars is None:
            self._init_solver()

        if self._previous_solution.is_empty():
            return Grid.empty()

        bool_vars = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                prev_val = self._previous_solution.value(r, c)
                diff_var = self._model.new_bool_var(f"diff_{r}_{c}_{len(self._model.Proto().variables)}")
                self._model.add(self._grid_vars.value(r, c) != prev_val).only_enforce_if(diff_var)
                self._model.add(self._grid_vars.value(r, c) == prev_val).only_enforce_if(diff_var.negated())
                bool_vars.append(diff_var)
        self._model.add_bool_or(bool_vars)

        return self._compute_solution()

    def _init_solver(self):
        num_regions = len(self._clues)
        self._grid_vars = Grid([[self._model.new_int_var(0, num_regions - 1, f"cell_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()

    def _compute_solution(self) -> Grid:
        solver = cp_model.CpSolver()
        status = solver.solve(self._model)
        if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            solution = Grid([[solver.value(self._grid_vars.value(r, c)) for c in range(self._columns_number)] for r in range(self._rows_number)])
            return solution
        return Grid.empty()

    def _add_constraints(self):
        self._add_region_constraints()
        self._add_no_four_corners_shared_constraint()

    def _add_region_constraints(self):
        for i, (pos, val) in enumerate(self._clues):
            r_min = self._model.new_int_var(0, self._rows_number - 1, f"r_min_{i}")
            r_max = self._model.new_int_var(0, self._rows_number - 1, f"r_max_{i}")
            c_min = self._model.new_int_var(0, self._columns_number - 1, f"c_min_{i}")
            c_max = self._model.new_int_var(0, self._columns_number - 1, f"c_max_{i}")

            self._model.add(r_min <= pos.r)
            self._model.add(r_max >= pos.r)
            self._model.add(c_min <= pos.c)
            self._model.add(c_max >= pos.c)
            self._model.add(r_min <= r_max)
            self._model.add(c_min <= c_max)

            height = self._model.new_int_var(1, self._rows_number, f"height_{i}")
            width = self._model.new_int_var(1, self._columns_number, f"width_{i}")
            self._model.add(height == r_max - r_min + 1)
            self._model.add(width == c_max - c_min + 1)

            is_horizontal = self._model.new_bool_var(f"is_horizontal_{i}")
            is_vertical = self._model.new_bool_var(f"is_vertical_{i}")

            self._model.add(height == 1).only_enforce_if(is_horizontal)
            self._model.add(width == 1).only_enforce_if(is_vertical)
            self._model.add_bool_or([is_horizontal, is_vertical])

            self._model.add(width != val).only_enforce_if(is_horizontal)
            self._model.add(height != val).only_enforce_if(is_vertical)

            for r in range(self._rows_number):
                for c in range(self._columns_number):
                    in_rect = self._model.new_bool_var(f"in_rect_{i}_{r}_{c}")

                    r_ge_min = self._model.new_bool_var(f"r_ge_min_{i}_{r}_{c}")
                    r_le_max = self._model.new_bool_var(f"r_le_max_{i}_{r}_{c}")
                    c_ge_min = self._model.new_bool_var(f"c_ge_min_{i}_{r}_{c}")
                    c_le_max = self._model.new_bool_var(f"c_le_max_{i}_{r}_{c}")

                    self._model.add(r >= r_min).only_enforce_if(r_ge_min)
                    self._model.add(r < r_min).only_enforce_if(r_ge_min.negated())
                    self._model.add(r <= r_max).only_enforce_if(r_le_max)
                    self._model.add(r > r_max).only_enforce_if(r_le_max.negated())
                    self._model.add(c >= c_min).only_enforce_if(c_ge_min)
                    self._model.add(c < c_min).only_enforce_if(c_ge_min.negated())
                    self._model.add(c <= c_max).only_enforce_if(c_le_max)
                    self._model.add(c > c_max).only_enforce_if(c_le_max.negated())

                    self._model.add_bool_and([r_ge_min, r_le_max, c_ge_min, c_le_max]).only_enforce_if(in_rect)
                    self._model.add_bool_or([r_ge_min.negated(), r_le_max.negated(), c_ge_min.negated(), c_le_max.negated()]).only_enforce_if(in_rect.negated())

                    self._model.add(self._grid_vars.value(r, c) == i).only_enforce_if(in_rect)
                    self._model.add(self._grid_vars.value(r, c) != i).only_enforce_if(in_rect.negated())

    def _add_no_four_corners_shared_constraint(self):
        for r in range(self._rows_number - 1):
            for c in range(self._columns_number - 1):
                a = self._grid_vars.value(r, c)
                b = self._grid_vars.value(r, c + 1)
                d = self._grid_vars.value(r + 1, c)
                e = self._grid_vars.value(r + 1, c + 1)

                ab_eq = self._model.new_bool_var(f"ab_eq_{r}_{c}")
                ad_eq = self._model.new_bool_var(f"ad_eq_{r}_{c}")
                ae_eq = self._model.new_bool_var(f"ae_eq_{r}_{c}")
                bd_eq = self._model.new_bool_var(f"bd_eq_{r}_{c}")
                be_eq = self._model.new_bool_var(f"be_eq_{r}_{c}")
                de_eq = self._model.new_bool_var(f"de_eq_{r}_{c}")

                self._model.add(a == b).only_enforce_if(ab_eq)
                self._model.add(a != b).only_enforce_if(ab_eq.negated())
                self._model.add(a == d).only_enforce_if(ad_eq)
                self._model.add(a != d).only_enforce_if(ad_eq.negated())
                self._model.add(a == e).only_enforce_if(ae_eq)
                self._model.add(a != e).only_enforce_if(ae_eq.negated())
                self._model.add(b == d).only_enforce_if(bd_eq)
                self._model.add(b != d).only_enforce_if(bd_eq.negated())
                self._model.add(b == e).only_enforce_if(be_eq)
                self._model.add(b != e).only_enforce_if(be_eq.negated())
                self._model.add(d == e).only_enforce_if(de_eq)
                self._model.add(d != e).only_enforce_if(de_eq.negated())

                self._model.add_bool_or([ab_eq, ad_eq, ae_eq, bd_eq, be_eq, de_eq])
