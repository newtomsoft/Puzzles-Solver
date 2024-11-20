from z3 import Solver, sat, Bool, is_true, Not, And

from Utils.Grid import Grid


class BinairoPlusGame:
    def __init__(self, grid: Grid, comparison_operators: dict[str, list[tuple[int, int]]]):
        self._grid = grid
        self._comparison_operators = comparison_operators
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 6:
            raise ValueError("Binairo+ grid must be at least 6x6")
        if self.rows_number % 2 != 0 or self.columns_number % 2 != 0:
            raise ValueError("Binairo+ grid must have an even number of rows/columns")
        self._solver = None
        self._matrix_z3 = None

    def get_solution(self) -> Grid:
        self._matrix_z3 = [[Bool(f"matrix_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._solver = Solver()
        self._add_constraints()
        if self._solver.check() != sat:
            return Grid.empty()

        return self._compute_solution()

    def _compute_solution(self) -> Grid:
        model = self._solver.model()
        solution = [[is_true(model.eval(self._matrix_z3[r][c])) for c in range(self.columns_number)] for r in range(self.rows_number)]
        return Grid(solution)

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_half_true_false_by_line_constraints()
        self._add_not_same_3_adjacent_constraints()
        self._add_comparison_operators_constraints()

    def _add_initial_constraints(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._grid.value(r, c) == 0:
                    self._solver.add(Not(self._matrix_z3[r][c]))
                elif self._grid.value(r, c) == 1:
                    self._solver.add(self._matrix_z3[r][c])

    def _add_half_true_false_by_line_constraints(self):
        half_columns = self.columns_number / 2
        half_rows = self.rows_number / 2
        for row_z3 in self._matrix_z3:
            self._solver.add(sum(row_z3[c] for c in range(self.columns_number)) == half_columns)
        for column_z3 in zip(*self._matrix_z3):
            self._solver.add(sum(column_z3[r] for r in range(self.rows_number)) == half_rows)

    def _add_not_same_3_adjacent_constraints(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number - 2):
                constraints = self._matrix_z3[r][c] == self._matrix_z3[r][c + 1], self._matrix_z3[r][c + 1] == self._matrix_z3[r][c + 2]
                constraint = And(constraints)
                not_constraint = Not(constraint)
                self._solver.add(not_constraint)
        for c in range(self.columns_number):
            for r in range(self.rows_number - 2):
                constraints = self._matrix_z3[r][c] == self._matrix_z3[r + 1][c], self._matrix_z3[r + 1][c] == self._matrix_z3[r + 2][c]
                constraint = And(constraints)
                not_constraint = Not(constraint)
                self._solver.add(not_constraint)

    def _add_comparison_operators_constraints(self):
        for r, c in self._comparison_operators['equal_on_columns'] if 'equal_on_columns' in self._comparison_operators else []:
            self._solver.add(self._matrix_z3[r][c] == self._matrix_z3[r + 1][c])
        for r, c in self._comparison_operators['non_equal_on_columns'] if 'non_equal_on_columns' in self._comparison_operators else []:
            self._solver.add(self._matrix_z3[r][c] != self._matrix_z3[r + 1][c])
        for r, c in self._comparison_operators['equal_on_rows'] if 'equal_on_rows' in self._comparison_operators else []:
            self._solver.add(self._matrix_z3[r][c] == self._matrix_z3[r][c + 1])
        for r, c in self._comparison_operators['non_equal_on_rows'] if 'non_equal_on_rows' in self._comparison_operators else []:
            self._solver.add(self._matrix_z3[r][c] != self._matrix_z3[r][c + 1])
