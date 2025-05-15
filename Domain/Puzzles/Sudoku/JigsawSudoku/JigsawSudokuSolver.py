from typing import List

from z3 import Distinct

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver
from Domain.Puzzles.Sudoku.SudokuBaseSolver import SudokuBaseSolver


class JigsawSudokuSolver(SudokuBaseSolver, GameSolver):
    def __init__(self, grid: Grid, regions: List[List[Position]]):
        super().__init__(grid)
        self._regions = regions
        if len(self._regions) != self.rows_number:
            raise ValueError("The grid must have the same number of regions as rows/column")
        if not self._are_regions_cells_count_compliant():
            raise ValueError("The regions must have the same number of cells")
        if not self._are_initial_numbers_different_in_region():
            raise ValueError("Initial numbers must be different in regions")

    def _add_specific_constraints(self):
        self._add_distinct_in_jigsaw_regions_constraints()

    def _add_distinct_in_jigsaw_regions_constraints(self):
        for region in self._regions:
            constraint = Distinct([self._grid_z3[position] for position in region])
            self._solver.add(constraint)

    def _are_regions_cells_count_compliant(self):
        return False if any(len(region) != self.rows_number for region in self._regions) else True

    def _are_initial_numbers_different_in_region(self):
        for region in self._regions:
            seen_in_region = []
            for position in region:
                value = self._grid.value(position.r, position.c)
                if value == -1:
                    continue
                if value in seen_in_region:
                    return False
                seen_in_region.append(value)
        return True
