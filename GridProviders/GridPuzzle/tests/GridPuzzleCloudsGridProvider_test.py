import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleCloudsGridProvider import GridPuzzleCloudsGridProvider

class GridPuzzleCloudsGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        expected_grid = [0, 3, 3, 3]
        grid = await self.run_scrap_test(GridPuzzleCloudsGridProvider, "clouds_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
