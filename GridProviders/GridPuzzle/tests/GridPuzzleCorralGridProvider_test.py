import unittest

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleCorralGridProvider import GridPuzzleCorralGridProvider
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase


class GridPuzzleCorralGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            [_, _, 2, _, _],
            [_, _, _, 5, _],
            [7, _, 7, _, _],
            [_, _, _, _, 5],
            [3, _, 3, _, _],
        ])
        grid = await self.run_scrap_test(GridPuzzleCorralGridProvider, "corral_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)


if __name__ == '__main__':
    unittest.main()
