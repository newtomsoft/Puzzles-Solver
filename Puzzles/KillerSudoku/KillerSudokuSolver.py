from typing import List, Dict, Tuple

from GameSolver import GameSolver
from Ports.SolverEngine import SolverEngine
from Sudoku.SudokuSolver import SudokuSolver
from Utils.Grid import Grid
from Utils.Position import Position


class KillerSudokuSolver(SudokuSolver, GameSolver):
    def __init__(self, grid: Grid, cages: Dict[int, Tuple[List[Position], int]], solver_engine: SolverEngine):
        super().__init__(grid, solver_engine)
        self.cages = cages
        if not self._are_cages_cover_grid():
            raise ValueError("The cages must cover the whole grid")
        if not self._are_initial_numbers_different_in_cage():
            raise ValueError("Initial numbers must be different in cages")

    def _add_specific_constraints(self):
        self._add_distinct_in_jigsaw_regions_constraints()

    def _add_distinct_in_jigsaw_regions_constraints(self):
        for cage, cage_sum in self.cages.values():
            constraint = self._solver.sum([self._grid_z3[position] for position in cage]) == cage_sum
            self._solver.add(constraint)

    def _are_initial_numbers_different_in_cage(self):
        for cage in [v[0] for v in self.cages.values()]:
            seen_in_region = []
            for position in cage:
                value = self._grid.value(position.r, position.c)
                if value == -1:
                    continue
                if value in seen_in_region:
                    return False
                seen_in_region.append(value)
        return True

    def _are_cages_cover_grid(self):
        return sum([len(cage[0]) for cage in self.cages.values()]) == self.rows_number * self.columns_number
