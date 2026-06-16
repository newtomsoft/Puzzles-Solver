import unittest

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.GridMask import is_outside_region, outside_from_grid, resolve_outside
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class GridMaskTest(unittest.TestCase):
    def test_outside_from_grid(self):
        grid = Grid([
            [GameSolver.cell_outside, 1],
            [0, GameSolver.cell_outside],
        ])
        self.assertEqual(outside_from_grid(grid), frozenset({(0, 0), (1, 1)}))

    def test_resolve_outside_merges_sources(self):
        grid = Grid([[GameSolver.cell_outside, 0], [0, 0]])
        self.assertEqual(
            resolve_outside(grid, {(1, 1)}),
            frozenset({(0, 0), (1, 1)}),
        )

    def test_is_outside_region(self):
        outside = frozenset({(0, 0)})
        from PuzzleSolver.Board.Position import Position

        self.assertTrue(is_outside_region([Position(0, 0)], outside))
        self.assertFalse(is_outside_region([Position(0, 0), Position(0, 1)], outside))


if __name__ == "__main__":
    unittest.main()