import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleRegionalYajilinGridProvider import GridPuzzleRegionalYajilinGridProvider

class GridPuzzleRegionalYajilinGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            [1, 1, 1, 2, 2],
            [1, 1, 1, 2, 2],
            [1, 1, 1, 2, 2],
            [1, 1, 1, 4, 4],
            [3, 3, 3, 4, 4],
        ])
        grid = await self.run_scrap_test(GridPuzzleRegionalYajilinGridProvider, "regionalyajilin_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
