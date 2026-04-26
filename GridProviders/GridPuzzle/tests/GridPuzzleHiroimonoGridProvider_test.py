import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleHiroimonoGridProvider import GridPuzzleHiroimonoGridProvider

class GridPuzzleHiroimonoGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            [_, _, _, _, 'S'],
            [_, 'S', _, 'S', _],
            [_, 'S', _, 'S', 'S'],
            ['S', _, _, 'S', _],
            [_, _, _, 'S', 'S']
        ])
        grid = await self.run_scrap_test(GridPuzzleHiroimonoGridProvider, "hiroimono_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
