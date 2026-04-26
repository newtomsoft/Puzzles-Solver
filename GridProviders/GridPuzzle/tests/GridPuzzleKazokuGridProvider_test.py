import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleKazokuGridProvider import GridPuzzleKazokuGridProvider

class GridPuzzleKazokuGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            [_, _, 1, _, _],
            [3, _, 0, _, 3],
            [_, _, 1, _, _],
            [_, _, _, _, _],
            [3, _, _, _, 1],
        ])
        grid = await self.run_scrap_test(GridPuzzleKazokuGridProvider, "kazoku_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
