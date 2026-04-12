import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleIrasutoGridProvider import GridPuzzleIrasutoGridProvider

class GridPuzzleIrasutoGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        # Le provider Irasuto retourne un tuple (num_grid, color_grid)
        num_grid, color_grid = await self.run_scrap_test(GridPuzzleIrasutoGridProvider, "irasuto_sample.html", "scrap_grid")
        
        self.assertIsNotNone(num_grid)
        self.assertIsInstance(num_grid, Grid)
        self.assertIsNotNone(color_grid)
        self.assertIsInstance(color_grid, Grid)

        # Grille de chiffres attendue pour https://gridpuzzle.com/irasuto/0y7x2
        expected_num_matrix = [
            [1, _, _, 2],
            [_, 2, 1, _],
            [_, _, _, _],
            [2, _, _, 0]
        ]
        self.assertEqual(Grid(expected_num_matrix), num_grid)

        # Grille de couleurs attendue
        expected_color_matrix = [
            ['w', 'w', 'w', 'b'],
            ['w', 'b', 'b', 'w'],
            ['w', 'w', 'w', 'w'],
            ['w', 'w', 'w', 'b']
        ]
        self.assertEqual(Grid(expected_color_matrix), color_grid)

if __name__ == '__main__':
    unittest.main()
