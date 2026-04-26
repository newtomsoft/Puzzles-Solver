import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleSeeThroughGridProvider import GridPuzzleSeeThroughGridProvider

class GridPuzzleSeeThroughGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            [2, 2],
            [2, 2],
        ])
        grid = await self.run_scrap_test(GridPuzzleSeeThroughGridProvider, "seethrough_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
