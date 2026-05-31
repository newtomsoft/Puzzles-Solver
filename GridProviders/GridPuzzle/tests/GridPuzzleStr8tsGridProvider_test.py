import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleStr8tsGridProvider import GridPuzzleStr8tsGridProvider

class GridPuzzleStr8tsGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            ['0', 3, 4, '0', '0'],
            [3, '0', '0', 2, 4],
            ['0', 2, 3, '0', '0'],
            ['0', '0', '0', 5, '0'],
            [5, '0', 2, '0', 1],
        ])
        grid = await self.run_scrap_test(GridPuzzleStr8tsGridProvider, "str8ts_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
