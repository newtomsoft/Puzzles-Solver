import unittest

from PuzzleSolver.Puzzles.DosunFuwari.DosunFuwariSolver import DosunFuwariSolver
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleDosunFuwariGridProvider import GridPuzzleDosunFuwariGridProvider

class GridPuzzleDosunFuwariGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = DosunFuwariSolver.empty
        expected_grid = Grid([
            [1, 1, 1, 2, 2],
            [3, 3, 4, 4, 5],
            [_, 3, 4, _, 5],
            [3, 3, 3, 6, 6],
            [3, 3, 3, 6, _]
        ])
        grid = await self.run_scrap_test(GridPuzzleDosunFuwariGridProvider, "dosunfuwari_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
