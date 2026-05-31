import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleSnakeGridProvider import GridPuzzleSnakeGridProvider

class GridPuzzleSnakeGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            [1, '0', '0'],
            ['0', '0', '0'],
            ['0', '0', 1],
        ])
        grid = await self.run_scrap_test(GridPuzzleSnakeGridProvider, "snake_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
