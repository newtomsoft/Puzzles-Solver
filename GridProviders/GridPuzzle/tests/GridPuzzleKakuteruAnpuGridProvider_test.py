import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleKakuteruAnpuGridProvider import GridPuzzleKakuteruAnpuGridProvider

class GridPuzzleKakuteruAnpuGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            [1, 1, 2, 2, 2],
            [3, 4, 5, 6, 2],
            [3, 4, 5, 6, 6],
            [4, 4, 7, 8, 8],
            [4, 7, 7, 7, 8],
        ])
        grid = await self.run_scrap_test(GridPuzzleKakuteruAnpuGridProvider, "kakuteruanpu_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
