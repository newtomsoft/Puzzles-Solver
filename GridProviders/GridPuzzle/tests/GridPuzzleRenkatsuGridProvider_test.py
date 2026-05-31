import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleRenkatsuGridProvider import GridPuzzleRenkatsuGridProvider

class GridPuzzleRenkatsuGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            [4, 5, 2, 2],
            [3, 1, 3, 4],
            [3, 1, 5, 1],
            [1, 4, 2, 2]
        ])
        grid = await self.run_scrap_test(GridPuzzleRenkatsuGridProvider, "renkatsu_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
