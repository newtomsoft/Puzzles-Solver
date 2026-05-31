import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleYajilinGridProvider import GridPuzzleYajilinGridProvider

class GridPuzzleYajilinGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            ['', '', '', '', '', '1L', '', ''],
            ['', '', '', '0R', '', '', '', ''],
            ['', '2R', '', '', '', '1L', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['1U', '', '', '', '', '1L', '0D', ''],
            ['', '', '', '0R', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['0R', '', '', '', '', '0L', '', '']
        ])
        grid = await self.run_scrap_test(GridPuzzleYajilinGridProvider, "yajilin_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
