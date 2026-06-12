from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Foseruzu.SameSizeRegionsSolver import SameSizeRegionsSolver
from PuzzleSolver.Puzzles.GameSolver import GameSolver

from .shapes import ALL_SHAPES, REGION_SIZE


class HekiSolver(SameSizeRegionsSolver):
    REGION_SIZE = REGION_SIZE
    ALL_SHAPES = ALL_SHAPES

    def __init__(self, grid: Grid):
        border_clues_grid = Grid([[4 - val if val != self.cell_empty and val != self.cell_empty else val for val in row] for row in grid.matrix])
        super().__init__(border_clues_grid)

    def _add_specific_constraints(self):
        self._add_two_clues_per_region_constraints()

    def _add_two_clues_per_region_constraints(self):
        for p, cells in enumerate(self._placements):
            clue_count = sum(1 for i, j in cells if self._grid[(i, j)] is not None)
            self._model.add(clue_count == 2).only_enforce_if(self._use[p])
