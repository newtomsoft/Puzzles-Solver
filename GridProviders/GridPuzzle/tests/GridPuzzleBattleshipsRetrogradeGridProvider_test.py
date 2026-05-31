import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleBattleshipsRetrogradeGridProvider import GridPuzzleBattleshipsRetrogradeGridProvider


class GridPuzzleBattleshipsRetrogradeGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        expected_grid = Grid([
            [3, 8, 4, 3, 4, 7, 1],
            [1, 3, 8, 8, 4, 7, 8],
            [8, 3, 4, 3, 4, 1, 2],
            [2, 7, 3, 4, 7, 8, 1],
            [7, 3, 8, 4, 7, 2, 2],
            [3, 4, 3, 8, 4, 7, 7],
            [7, 3, 4, 7, 3, 4, 7],
        ])
        expected_ships = {1: 3, 2: 2, 3: 1, 4: 1}
        result = await self.run_scrap_test(GridPuzzleBattleshipsRetrogradeGridProvider, 'battleships_retrograde_sample.html', 'scrap_grid')
        grid, ships_number_by_size = result
        self.assert_grid_equals(expected_grid, grid)
        self.assertEqual(expected_ships, ships_number_by_size)


if __name__ == '__main__':
    unittest.main()
