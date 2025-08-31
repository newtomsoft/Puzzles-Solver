from z3 import Solver, Int, Not, And, Distinct, sat

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
        self._symbol_region_ids: dict | None = self._compute_symbol_region_ids()

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
        if self._grid_z3 is None:
            return Grid.empty()
        check_result = self._solver.check()
        if check_result == sat:
            model = self._solver.model()
            solution = []
            for r in range(self._rows_number):
                row_vals = []
                for c in range(self._columns_number):
                    v = model.eval(self._grid_z3.value(r, c))

                    try:
                        row_vals.append(int(str(v)))
                    except Exception:
                        try:
                            row_vals.append(int(v.as_long()))
                        except Exception:
                            row_vals.append(0)
                solution.append(row_vals)
            return Grid(solution)
        return Grid.empty()

    def _add_constraints(self):
        self._add_grid_bounds_constraints()
        self._add_value_at_symbols_constraints()
        self._add_region_shape_constraints()
        self._add_no_four_corners_shared_constraint()

    def _add_grid_bounds_constraints(self):
        symbols_count = 0
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                val = self._initial_grid.value(r, c)
                if val in ['+', '-', '|']:
                    symbols_count += 1
        max_id = symbols_count
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                v = self._grid_z3.value(r, c)
                self._solver.add(And(v >= 1, v <= max_id))

    def _add_value_at_symbols_constraints(self):
        for index, (position, symbol) in enumerate(self._symbol_region_ids.items()):
            cell_id = self._grid_z3[position]
            self._solver.add(cell_id == index + 1)

    def _add_region_shape_constraints(self):
        for position, symbol in self._symbol_region_ids.items():
            if symbol == '+':
                continue

            if symbol == '-':
                continue

            if symbol == '|':
                continue

    def _add_no_four_corners_shared_constraint(self):
        for r in range(self._rows_number - 1):
            for c in range(self._columns_number - 1):
                a = self._grid_z3.value(r, c)
                b = self._grid_z3.value(r, c + 1)
                d = self._grid_z3.value(r + 1, c)
                e = self._grid_z3.value(r + 1, c + 1)
                self._solver.add(Not(Distinct(a, b, d, e)))
