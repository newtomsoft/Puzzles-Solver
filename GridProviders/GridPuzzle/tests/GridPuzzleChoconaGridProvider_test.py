import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleChoconaGridProvider import GridPuzzleChoconaGridProvider

class GridPuzzleChoconaGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            [4, '-1', '-1', 1],
            ['-1', '-1', '-1', '-1'],
            [1, 1, 3, '-1'],
            ['-1', '-1', '-1', '-1'],
        ])
        grid = await self.run_scrap_test(GridPuzzleChoconaGridProvider, "chocona_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
