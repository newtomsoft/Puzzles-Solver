import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleHakoiriGridProvider import GridPuzzleHakoiriGridProvider

class GridPuzzleHakoiriGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            [0, 2, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 3, 1, 0],
        ])
        _, grid = await self.run_scrap_test(GridPuzzleHakoiriGridProvider, "hakoiri_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
