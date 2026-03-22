import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleSummandumGridProvider import GridPuzzleSummandumGridProvider

class GridPuzzleSummandumGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_4x4_with_mock(self):
        _ = None
        grid = await self.run_scrap_test(GridPuzzleSummandumGridProvider, "summandum_sample.html", "scrap_grid")
        expected_grid = Grid([
            [3, _, 2, 0],
            [_, 4, _, 3],
            [4, _, 3, _],
            [5, 3, _, 2]
        ])
        self.assertEqual(expected_grid, grid)
