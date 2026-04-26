import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleMintonetteGridProvider import GridPuzzleMintonetteGridProvider

class GridPuzzleMintonetteGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            [1, 'MintonetteSolver.Empty', 0, 0],
            [0, 1, 'MintonetteSolver.Empty', 4],
            ['MintonetteSolver.Empty', 'MintonetteSolver.Empty', 'MintonetteSolver.Empty', 0],
            [0, 'MintonetteSolver.Empty', 4, 0],
        ])
        grid = await self.run_scrap_test(GridPuzzleMintonetteGridProvider, "mintonette_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
