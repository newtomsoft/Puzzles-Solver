from z3 import Bool, Solver, Not, sat, is_true, Sum, Implies, Or

from Utils.Grid import Grid
from Utils.Position import Position


class ThermometersGame:
    _tree_value = -1

    def __init__(self, grid: Grid, tents_numbers_by_column_row):
        self._grid: Grid = grid
        self.tents_numbers_by_column_row: dict[str, list[int]] = tents_numbers_by_column_row
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 4:
            raise ValueError("The grid must be at least 4x4")
        self.columns_tents_numbers = self.tents_numbers_by_column_row['column']
        self.rows_tents_numbers = self.tents_numbers_by_column_row['row']
        self._solver = None
        self._grid_z3 = None