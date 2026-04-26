import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleCountryRoadGridProvider import GridPuzzleCountryRoadGridProvider

class GridPuzzleCountryRoadGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            [4, _, _, _],
            [_, 1, _, 3],
            [1, 2, 1, _],
            [_, _, _, _]
        ])
        grid = await self.run_scrap_test(GridPuzzleCountryRoadGridProvider, "countryroad_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
