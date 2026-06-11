from .shapes import ALL_SHAPES, REGION_SIZE
from PuzzleSolver.Puzzles.Foseruzu.SameSizeRegionsSolver import SameSizeRegionsSolver


class FiveCellsSolver(SameSizeRegionsSolver):
    REGION_SIZE = REGION_SIZE
    ALL_SHAPES = ALL_SHAPES
    # Original data lives in shapes.json (loaded by shapes.py).
    # The values are assigned to class attributes for SameSizeRegionsSolver compatibility.