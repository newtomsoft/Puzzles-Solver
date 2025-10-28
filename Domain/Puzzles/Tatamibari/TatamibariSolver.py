from collections import defaultdict

from z3 import Solver, Int, Not, And, Distinct, sat

from Domain.Board.Position import Position
from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class TatamibariSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._initial_grid = grid
        self._rows_number = grid.rows_number
        self._columns_number = grid.columns_number
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None
        self._symbol_by_position: dict | None = self._compute_symbol_region_ids()
        self._region_id_by_position: defaultdict[Position, int] = defaultdict(int)

    def _compute_symbol_region_ids(self):
        symbol_region_ids: dict = {}
        for position, value in [(position, value) for position, value in self._initial_grid if value in ['+', '-', '|']]:
            symbol_region_ids[position] = value
        return symbol_region_ids

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()
        solution = self._compute_solution()
        self._previous_solution = solution
        return solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()

        if not self._solver.assertions():
            self._init_solver()

        equalities = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                try:
                    v = self._previous_solution.value(r, c)
                except Exception:
                    v = None
                if v is not None:
                    equalities.append(self._grid_z3.value(r, c) == v)
        if equalities:
            self._solver.add(Not(And(equalities)))

        return self._compute_solution()

    def _init_solver(self):
        self._grid_z3 = Grid([[Int(f"cell_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()

    def _compute_solution(self) -> Grid:
        check_result = self._solver.check()
        if check_result == sat:
            model = self._solver.model()
            solution = Grid([[model.evaluate(self._grid_z3.value(r, c)).as_long() for c in range(self._columns_number)] for r in range(self._rows_number)])
            return solution
        return Grid.empty()

    def _add_constraints(self):
        self._add_grid_bounds_constraints()
        self._add_value_at_symbols_constraints()
        self._add_no_four_corners_shared_constraint()
        self._add_region_shape_constraints()

    def _add_grid_bounds_constraints(self):
        max_id = len(self._symbol_by_position)
        for position, value in self._grid_z3:
            self._solver.add(And(value >= 1, value <= max_id))

    def _add_value_at_symbols_constraints(self):
        for index, (position, symbol) in enumerate(self._symbol_by_position.items()):
            cell_id = self._grid_z3[position]
            self._solver.add(cell_id == index + 1)
            self._region_id_by_position[position] = index + 1

    def _add_no_four_corners_shared_constraint(self):
        for r in range(self._rows_number - 1):
            for c in range(self._columns_number - 1):
                a = self._grid_z3.value(r, c)
                b = self._grid_z3.value(r, c + 1)
                d = self._grid_z3.value(r + 1, c)
                e = self._grid_z3.value(r + 1, c + 1)
                self._solver.add(Not(Distinct(a, b, d, e)))

    def _add_region_shape_constraints(self):
        for position, symbol in self._symbol_by_position.items():
            self._add_region_rectangle_constraints(position, symbol)

    def _add_region_rectangle_constraints(self, position, symbol):
        region_id = self._region_id_by_position[position]

        left_row = Int(f"rect_r0_{region_id}")
        top_column = Int(f"rect_c0_{region_id}")
        height = Int(f"rect_h_{region_id}")
        width = Int(f"rect_w_{region_id}")

        match symbol:
            case '-':
                self._solver.add(width > height)
            case '|':
                self._solver.add(height > width)
            case '+':
                self._solver.add(width == height)
            case _:
                raise ValueError(f"Unexpected symbol '{symbol}' at position {position}")

        self._add_rectangle_in_grid_constraints(height, width, left_row, top_column)

        for r in range(self._rows_number):
            for c in range(self._columns_number):
                cell_is_region = self._grid_z3.value(r, c) == region_id
                inside_rectangle = And(left_row <= r, r < left_row + height, top_column <= c, c < top_column + width)
                self._solver.add(cell_is_region == inside_rectangle)

    def _add_rectangle_in_grid_constraints(self, rectangle_height, rectangle_width, left_row, top_column):
        self._solver.add(left_row >= 0)
        self._solver.add(top_column >= 0)
        self._solver.add(rectangle_height >= 1)
        self._solver.add(rectangle_width >= 1)
        self._solver.add(left_row + rectangle_height <= self._rows_number)
        self._solver.add(top_column + rectangle_width <= self._columns_number)
