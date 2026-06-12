from .shapes import ALL_SHAPES, REGION_SIZE
from PuzzleSolver.Puzzles.Foseruzu.SameSizeRegionsSolver import SameSizeRegionsSolver


class FiveCellsSolver(SameSizeRegionsSolver):
    REGION_SIZE = REGION_SIZE
    ALL_SHAPES = ALL_SHAPES

    def _add_specific_constraints(self):
        pass