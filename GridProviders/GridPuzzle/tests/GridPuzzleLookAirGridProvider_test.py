import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleLookAirGridProvider import GridPuzzleLookAirGridProvider

class GridPuzzleLookAirGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            [3, '-1', '-1', '-1', 1],
            ['-1', 3, '-1', 1, '-1'],
            [1, '-1', 1, '-1', 3],
            [2, '-1', 2, 3, '-1'],
            [1, 2, '-1', '-1', 1],
        ])
        grid = await self.run_scrap_test(GridPuzzleLookAirGridProvider, "lookair_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
