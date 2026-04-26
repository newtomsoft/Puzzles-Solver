import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleTilePaintGridProvider import GridPuzzleTilePaintGridProvider

class GridPuzzleTilePaintGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            [1, 2, 3, 3, 4, 4, 5, 5],
            [1, 2, 6, 3, 3, 7, 5, 5],
            [2, 2, 6, 8, 8, 7, 9, 9],
            [10, 11, 12, 8, 8, 9, 9, 13],
            [10, 11, 12, 14, 15, 15, 16, 13],
            [10, 10, 12, 14, 14, 15, 16, 16],
            [17, 18, 12, 19, 20, 15, 21, 21],
            [17, 18, 19, 19, 20, 20, 21, 21]
        ])
        grid = await self.run_scrap_test(GridPuzzleTilePaintGridProvider, "tilepaint_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
