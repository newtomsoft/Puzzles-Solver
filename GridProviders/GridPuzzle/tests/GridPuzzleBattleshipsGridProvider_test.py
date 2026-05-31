import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Bimaru.BimaruSolver import BimaruSolver
from GridProviders.GridPuzzle.GridPuzzleBattleshipsGridProvider import GridPuzzleBattleshipsGridProvider


_ = -1


class GridPuzzleBattleshipsGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        expected_grid = Grid([
            [_, _, _, _, _, BimaruSolver.ship_single],
            [_, BimaruSolver.ship_right, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, BimaruSolver.ship_middle_input, _, _, _],
        ])
        expected_ship_cells = {
            'row': [1, 3, 0, 4, 0, 3],
            'column': [1, 3, 2, 3, 1, 1],
        }
        expected_ships_by_size = {1: 2, 2: 1, 3: 1, 4: 1}

        result = await self.run_scrap_test(GridPuzzleBattleshipsGridProvider, 'battleships_sample.html', 'scrap_grid')
        grid, ship_cells, ships_by_size = result
        self.assert_grid_equals(expected_grid, grid)
        self.assertEqual(expected_ship_cells, ship_cells)
        self.assertEqual(expected_ships_by_size, ships_by_size)


if __name__ == '__main__':
    unittest.main()
