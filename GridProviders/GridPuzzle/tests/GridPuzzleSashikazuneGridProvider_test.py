import unittest
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from GridProviders.GridPuzzle.GridPuzzleSashikazuneGridProvider import GridPuzzleSashikazuneGridProvider

class GridPuzzleSashikazuneGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid(self):
        _ = None
        expected_grid = Grid([
            [5, 1, _, _, 2],
            [4, 2, _, 2, _],
            [_, 3, _, 2, _],
            [_, 3, _, 1, 2],
            [1, _, _, 2, 3]
        ])
        grid = await self.run_scrap_test(GridPuzzleSashikazuneGridProvider, "sashikazune_sample.html")
        
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
