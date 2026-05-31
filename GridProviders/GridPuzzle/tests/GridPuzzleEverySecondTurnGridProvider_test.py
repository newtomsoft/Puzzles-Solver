import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleEverySecondTurnGridProvider import GridPuzzleEverySecondTurnGridProvider

class GridPuzzleEverySecondTurnGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        expected_grid = Grid([
            ['.', '.', '.', '.', '.', '*'],
            ['.', '*', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '*', '.'],
            ['*', '.', '.', '*', '.', '.'],
            ['.', '.', '*', '.', '.', '*'],
            ['*', '.', '.', '.', '.', '.'],
        ])
        grid = await self.run_scrap_test(GridPuzzleEverySecondTurnGridProvider, "everysecondturn_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
