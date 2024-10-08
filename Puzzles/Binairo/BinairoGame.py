from z3 import Solver, sat, Sum, Bool, BitVec, Extract

from Grid import Grid


class BinairoGame:
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("Binairo grid must be square")
        if self.rows_number < 2:
            raise ValueError("Binairo grid must be at least 6x6")
        self._solver = None
        self._rows_z3: list[BitVec] = []
        self._columns_z3: list[BitVec] = []

    def get_solution(self) -> (Grid | None, int):
        self._rows_z3 = [BitVec(f"row_{r}", self.columns_number) for r in range(self.rows_number)]
        self._columns_z3 = [BitVec(f"column_{c}", self.rows_number) for c in range(self.columns_number)]
        self._solver = Solver()
        self._add_constraints()
        if self._solver.check() != sat:
            return None
        model = self._solver.model()
        rows = []
        for i_row in range(self.rows_number):
            row_value = model[self._rows_z3[i_row]].as_long()
            row_list = [(row_value >> j) & 1 == 1 for j in range(self.columns_number - 1, -1, -1)]
            rows.append(row_list)
        return Grid(rows)

    def _add_constraints(self):
        self._add_row_column_intersection_constraints()
        self._add_constraint_sums_by_rows()

    def _add_row_column_intersection_constraints(self):
        constraints_extract = []
        for i_row in range(self.rows_number):
            index_row = self.rows_number - i_row - 1
            for i_col in range(self.columns_number):
                index_col = self.columns_number - i_col - 1
                cons_extract = Extract(index_col, index_col, self._rows_z3[i_row]) == Extract(index_row, index_row, self._columns_z3[i_col])
                constraints_extract.append(cons_extract)
        self._solver.add(constraints_extract)

    def _add_constraint_sums_by_rows(self):
        constraints = []
        for r in range(self.rows_number):
            constraints.append(Sum([self._rows_z3.value(r, c) * self._grid.value(r, c) for c in range(self.columns_number)]) == self._column_sums[r])
        self._solver.add(constraints)

