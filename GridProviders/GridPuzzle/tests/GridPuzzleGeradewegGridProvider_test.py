import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleGeradewegGridProvider import GridPuzzleGeradewegGridProvider

class GridPuzzleGeradewegGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        expected_grid = Grid([
            ['0', '0', '0', '0'],
            ['0', 1, 1, '0'],
            [2, '0', '0', 1],
            ['0', 3, 3, '0']
        ])
        grid = await self.run_scrap_test(GridPuzzleGeradewegGridProvider, "geradeweg_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
