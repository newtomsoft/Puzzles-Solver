import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleToichikaGridProvider import GridPuzzleToichikaGridProvider


class GridPuzzleToichikaGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        expected_regions_grid_str = (
            '┌───┬─┬─┬─┐\n'
            '├───┤ │ └─┤\n'
            '├─┐ │ │ ┌─┤\n'
            '│ └─┤ ├─┘ │\n'
            '│ ┌─┴─┴─┐ │\n'
            '└─┴─────┴─┘\n'
        )
        expected_given_arrows = Grid([
            [0, 0, 0, 0, 0],
            [3, 0, 0, 0, 4],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0],
            [0, 0, 0, 0, 0],
        ])

        regions_grid, given_arrows = await self.run_scrap_test(GridPuzzleToichikaGridProvider, "toichika_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_regions_grid_str, str(regions_grid))
        self.assert_grid_equals(expected_given_arrows, given_arrows)


if __name__ == '__main__':
    unittest.main()
