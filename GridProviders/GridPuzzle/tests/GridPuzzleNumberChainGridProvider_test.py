import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleNumberChainGridProvider import GridPuzzleNumberChainGridProvider

class GridPuzzleNumberChainGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            [1, 3, 8, 4],
            [9, 10, 7, 2],
            [3, 2, 6, 10],
            [7, 1, 5, 11]
        ])
        grid = await self.run_scrap_test(GridPuzzleNumberChainGridProvider, "numberchain_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
