import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleMobiritiGridProvider import GridPuzzleMobiritiGridProvider

class GridPuzzleMobiritiGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        num_grid = await self.run_scrap_test(GridPuzzleMobiritiGridProvider, "mobiriti_sample.html", "scrap_grid")
        
        self.assertIsNotNone(num_grid)
        self.assertIsInstance(num_grid, Grid)

        # Grille de chiffres attendue pour https://gridpuzzle.com/mobiriti/3jnr9 (5x5)
        expected_num_matrix = [
            [_, 2, _, _, _],
            [1, _, 1, 3, _],
            [1, _, 3, _, _],
            [_, 3, _, _, _],
            [_, _, 3, _, 1]
        ]
        self.assertEqual(Grid(expected_num_matrix), num_grid)

if __name__ == '__main__':
    unittest.main()
