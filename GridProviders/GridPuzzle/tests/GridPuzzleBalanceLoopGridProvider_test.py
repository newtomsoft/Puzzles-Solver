import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleBalanceLoopGridProvider import GridPuzzleBalanceLoopGridProvider

class GridPuzzleBalanceLoopGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            ['b6', 'b4', 'w4', 'b4', 'b6'],
            [_, _, 'b3', _, _],
            ['b3', _, _, _, 'b3'],
            [_, _, _, _, _],
            [_, 'b4', _, 'b3', _],
        ])
        grid = await self.run_scrap_test(GridPuzzleBalanceLoopGridProvider, "balanceloop_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
