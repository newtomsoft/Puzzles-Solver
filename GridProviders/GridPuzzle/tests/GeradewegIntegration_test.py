import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleGeradewegGridProvider import GridPuzzleGeradewegGridProvider
from Domain.Puzzles.Geradeweg.GeradewegSolver import GeradewegSolver

class GeradewegIntegrationTests(GridPuzzleProviderTestBase):
    async def test_scrap_and_solve_geradeweg(self):
        # 1. Utiliser le provider pour scraper la grille à partir d'un fichier HTML local
        grid = await self.run_scrap_test(GridPuzzleGeradewegGridProvider, "geradeweg_sample.html", "scrap_grid")
        
        self.assertIsNotNone(grid)
        self.assertIsInstance(grid, Grid)

        # 2. Initialiser le solver avec la grille scrapée
        solver = GeradewegSolver(grid)
        
        # 3. Obtenir la solution
        solution = solver.get_solution()
        
        # 4. Vérifications
        self.assertIsNotNone(solution)
        self.assertFalse(solution.is_empty(), "Le solver devrait trouver une solution pour la grille sample.")
        
        # Vérification des dimensions
        self.assertEqual(solution.rows_number, grid.rows_number)
        self.assertEqual(solution.columns_number, grid.columns_number)

if __name__ == '__main__':
    unittest.main()
