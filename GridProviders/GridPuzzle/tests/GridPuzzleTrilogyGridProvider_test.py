import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleTrilogyGridProvider import GridPuzzleTrilogyGridProvider

class GridPuzzleTrilogyGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            ['1', '0', '0', '1'],
            ['2', '0', '0', '3'],
            ['1', '0', '0', '1'],
            ['1', '3', '1', '1']
        ])
        grid = await self.run_scrap_test(GridPuzzleTrilogyGridProvider, "trilogy_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
