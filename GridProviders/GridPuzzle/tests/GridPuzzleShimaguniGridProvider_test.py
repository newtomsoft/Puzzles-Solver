import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleShimaguniGridProvider import GridPuzzleShimaguniGridProvider

class GridPuzzleShimaguniGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            [3, _, 2, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [1, _, _, _, _],
            [4, _, _, 3, _],
        ])
        expected_regions_grid_str = (
        '┌───┬───┬─┐\n'
        '│   │   ├─┤\n'
        '│ ┌─┴───┤ │\n'
        '├─┘ ┌───┤ │\n'
        '├───┘ ┌─┘ │\n'
        '└─────┴───┘\n'
        )

        clues_grid, regions_grid = await self.run_scrap_test(GridPuzzleShimaguniGridProvider, "shimaguni_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, clues_grid)
        self.assert_grid_equals(expected_regions_grid_str, str(regions_grid))

if __name__ == '__main__':
    unittest.main()
