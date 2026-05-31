import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleMoonsunGridProvider import GridPuzzleMoonsunGridProvider

class GridPuzzleMoonsunGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            [1, 1, 1, 2, 3],
            [1, 1, 2, 2, 3],
            [1, 4, 4, 5, 6],
            [1, 1, 4, 7, 6],
            [1, 4, 4, 8, 6],
        ])
        grid = await self.run_scrap_test(GridPuzzleMoonsunGridProvider, "moonsun_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
