import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleIrasutoGridProvider import GridPuzzleIrasutoGridProvider
from Domain.Puzzles.Irasuto.IrasutoSolver import IrasutoSolver

class IrasutoIntegrationTests(GridPuzzleProviderTestBase):
    async def test_scrap_and_solve_irasuto(self):
        # 1. Utiliser le provider pour scraper la grille à partir d'un fichier HTML local
        # Ce fichier "irasuto_sample.html" devrait exister dans GridProviders/GridPuzzle/tests/assets/
        num_grid, color_grid = await self.run_scrap_test(GridPuzzleIrasutoGridProvider, "irasuto_sample.html", "scrap_grid")
        
        self.assertIsNotNone(num_grid)
        self.assertIsInstance(num_grid, Grid)
        self.assertIsNotNone(color_grid)
        self.assertIsInstance(color_grid, Grid)

        # 2. Initialiser le solver avec la grille scrapée
        solver = IrasutoSolver(num_grid, color_grid)
        
        # 3. Obtenir la solution
        solution = solver.get_solution()
        
        # 4. Vérifications
        self.assertIsNotNone(solution)
        self.assertNotEqual(solution, Grid.empty(), "Le solver devrait trouver une solution pour la grille sample.")
        
        # Grid from https://gridpuzzle.com/irasuto/0y7x2
        w = 'w'
        b = 'b'
        expected_solution = Grid([
            [w, b, b, b],
            [w, b, b, w],
            [b, b, w, w],
            [w, w, w, b]
        ])
        self.assertEqual(expected_solution, solution)

        # Vérification supplémentaire : la grille de solution doit avoir les mêmes dimensions
        self.assertEqual(solution.rows_number, num_grid.rows_number)
        self.assertEqual(solution.columns_number, num_grid.columns_number)

if __name__ == '__main__':
    unittest.main()
