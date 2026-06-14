import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleYakuzuGridProvider import GridPuzzleYakuzuGridProvider


class GridPuzzleYakuzuGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        # Uses the yakazu_sample.html which encodes the user's example grid
        # _ 3 _ 2 _ | 4 # 2 # 2 | 5 # _ # 3 | _ 3 _ 5 _ | 3 # 1 # 5
        grid = await self.run_scrap_test(GridPuzzleYakuzuGridProvider, "yakazu_sample.html", "scrap_grid")
        expected_grid = Grid([
            [0, 3, 0, 2, 0],
            [4, 0, 2, 0, 2],
            [5, 0, 0, 0, 3],
            [0, 3, 0, 5, 0],
            [3, 0, 1, 0, 5],
        ])
        self.assert_grid_equals(expected_grid, grid)


if __name__ == '__main__':
    unittest.main()
