import unittest

from Domain.Puzzles.BorderBlock.BorderBlockSolver import BorderBlockSolver
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleBorderBlockGridProvider import GridPuzzleBorderBlockGridProvider

class GridPuzzleBorderBlockGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = BorderBlockSolver.empty
        expected_grid = Grid([
            [_, 3, _, 3, _],
            [_, 3, 6, 5, _],
            [7, _, _, _, 1],
            [_, _, 6, _, _],
            [2, _, 4, _, 4]
        ])
        grid = await self.run_scrap_test(GridPuzzleBorderBlockGridProvider, "borderblock_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
