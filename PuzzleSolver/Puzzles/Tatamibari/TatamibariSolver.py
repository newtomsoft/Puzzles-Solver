from collections import defaultdict

from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class TatamibariSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._initial_grid = grid
        self._rows_number = grid.rows_number
        self._columns_number = grid.columns_number
        self._model = cp_model.CpModel()
        self._grid_vars: Grid | None = None
        self._previous_solution: Grid | None = None
        self._symbol_by_position: dict | None = self._compute_symbol_region_ids()
        self._region_id_by_position: defaultdict[Position, int] = defaultdict(int)

    def _compute_symbol_region_ids(self):
        symbol_region_ids: dict = {}
        for position, value in [(position, value) for position, value in self._initial_grid if value in ['+', '-', '|']]:
            symbol_region_ids[position] = value
        return symbol_region_ids

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
        max_id = len(self._symbol_by_position)
        self._grid_vars = Grid([[self._model.new_int_var(1, max_id, f"cell_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()

    def _compute_solution(self) -> Grid:
        solver = cp_model.CpSolver()
        status = solver.solve(self._model)
        if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            solution = Grid([[solver.value(self._grid_vars.value(r, c)) for c in range(self._columns_number)] for r in range(self._rows_number)])
            return solution
        return Grid.empty()

    def _add_constraints(self):
        self._add_value_at_symbols_constraints()
        self._add_no_four_corners_shared_constraint()
        self._add_region_shape_constraints()

    def _add_value_at_symbols_constraints(self):
        for index, (position, symbol) in enumerate(self._symbol_by_position.items()):
            cell_id = self._grid_vars[position]
            self._model.add(cell_id == index + 1)
            self._region_id_by_position[position] = index + 1

    def _add_no_four_corners_shared_constraint(self):
        for r in range(self._rows_number - 1):
            for c in range(self._columns_number - 1):
                a = self._grid_vars.value(r, c)
                b = self._grid_vars.value(r, c + 1)
                d = self._grid_vars.value(r + 1, c)
                e = self._grid_vars.value(r + 1, c + 1)

                # Not all different, so at least one pair is equal
                ab_eq = self._model.new_bool_var('')
                ad_eq = self._model.new_bool_var('')
                ae_eq = self._model.new_bool_var('')
                bd_eq = self._model.new_bool_var('')
                be_eq = self._model.new_bool_var('')
                de_eq = self._model.new_bool_var('')

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

    def _add_region_shape_constraints(self):
        for position, symbol in self._symbol_by_position.items():
            self._add_region_rectangle_constraints(position, symbol)

    def _add_region_rectangle_constraints(self, position, symbol):
        region_id = self._region_id_by_position[position]

        left_row = self._model.new_int_var(0, self._rows_number - 1, f"rect_r0_{region_id}")
        top_column = self._model.new_int_var(0, self._columns_number - 1, f"rect_c0_{region_id}")
        height = self._model.new_int_var(1, self._rows_number, f"rect_h_{region_id}")
        width = self._model.new_int_var(1, self._columns_number, f"rect_w_{region_id}")

        match symbol:
            case '-':
                self._model.add(width > height)
            case '|':
                self._model.add(height > width)
            case '+':
                self._model.add(width == height)
            case _:
                raise ValueError(f"Unexpected symbol '{symbol}' at position {position}")

        self._add_rectangle_in_grid_constraints(height, width, left_row, top_column)

        for r in range(self._rows_number):
            for c in range(self._columns_number):
                cell_is_region = self._model.new_bool_var(f"cell_is_region_{r}_{c}_{region_id}")
                inside_rectangle = self._model.new_bool_var(f"inside_rectangle_{r}_{c}_{region_id}")

                self._model.add(self._grid_vars.value(r, c) == region_id).only_enforce_if(cell_is_region)
                self._model.add(self._grid_vars.value(r, c) != region_id).only_enforce_if(cell_is_region.negated())

                # inside_rectangle <=> (left_row <= r < left_row + height) and (top_column <= c < top_column + width)
                r_in = self._model.new_bool_var('')
                self._model.add(r >= left_row).only_enforce_if(r_in)
                self._model.add(r < left_row).only_enforce_if(r_in.negated())

                r_out = self._model.new_bool_var('')
                self._model.add(r < left_row + height).only_enforce_if(r_out)
                self._model.add(r >= left_row + height).only_enforce_if(r_out.negated())

                c_in = self._model.new_bool_var('')
                self._model.add(c >= top_column).only_enforce_if(c_in)
                self._model.add(c < top_column).only_enforce_if(c_in.negated())

                c_out = self._model.new_bool_var('')
                self._model.add(c < top_column + width).only_enforce_if(c_out)
                self._model.add(c >= top_column + width).only_enforce_if(c_out.negated())

                self._model.add_bool_and([r_in, r_out, c_in, c_out]).only_enforce_if(inside_rectangle)
                self._model.add_bool_or([r_in.negated(), r_out.negated(), c_in.negated(), c_out.negated()]).only_enforce_if(inside_rectangle.negated())

                self._model.add(cell_is_region == inside_rectangle)

    def _add_rectangle_in_grid_constraints(self, rectangle_height, rectangle_width, left_row, top_column):
        self._model.add(left_row >= 0)
        self._model.add(top_column >= 0)
        self._model.add(rectangle_height >= 1)
        self._model.add(rectangle_width >= 1)
        self._model.add(left_row + rectangle_height <= self._rows_number)
        self._model.add(top_column + rectangle_width <= self._columns_number)
