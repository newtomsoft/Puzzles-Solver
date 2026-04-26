import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleYajikabeGridProvider import GridPuzzleYajikabeGridProvider

class GridPuzzleYajikabeGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            ['1↓', '', '4↓', '', '1←'],
            ['', '', '', '', ''],
            ['', '0↓', '', '0↑', ''],
            ['', '', '', '', ''],
            ['1↑', '', '', '', '3↑'],
        ])
        grid = await self.run_scrap_test(GridPuzzleYajikabeGridProvider, "yajikabe_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
