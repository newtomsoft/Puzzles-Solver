import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleCreekGridProvider import GridPuzzleCreekGridProvider

class GridPuzzleCreekGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        X = -1
        expected_grid = Grid([
            [0, X, 0, X, 0],
            [1, 2, 1, 1, 1],
            [X, 3, X, 1, X],
            [1, X, 1, X, 0],
            [0, 0, 1, 1, 0]
        ])
        grid = await self.run_scrap_test(GridPuzzleCreekGridProvider, "creek_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
