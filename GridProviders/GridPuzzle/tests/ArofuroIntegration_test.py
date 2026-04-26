import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleArofuroGridProvider import GridPuzzleArofuroGridProvider
from Domain.Puzzles.Arofuro.ArofuroSolver import ArofuroSolver

class ArofuroIntegrationTests(GridPuzzleProviderTestBase):
    async def test_scrap_and_solve_arofuro(self):
        # 1. Utiliser le provider pour scraper la grille à partir d'un fichier HTML local
        # Ce fichier "arofuro_sample.html" devrait exister dans GridProviders/GridPuzzle/tests/assets/
        grid = await self.run_scrap_test(GridPuzzleArofuroGridProvider, "arofuro_sample.html", "scrap_grid")
        
        self.assertIsNotNone(grid)
        self.assertIsInstance(grid, Grid)

        # 2. Initialiser le solver avec la grille scrapée
        solver = ArofuroSolver(grid)
        
        # 3. Obtenir la solution
        solution = solver.get_solution()
        
        # 4. Vérifications
        self.assertIsNotNone(solution)
        self.assertNotEqual(solution, Grid.empty(), "Le solver devrait trouver une solution pour la grille sample.")
        
        # Grid from https://gridpuzzle.com/arofuro/375gk
        expected_solution_str = (
            '• ← → • \n'
            '• → ↑ • \n'
            '→ ↓ ← ↓ \n'
            '• ← ↑ • '
        )
        self.assertEqual(expected_solution_str, solver.solution_to_string())

        # Vérification supplémentaire : la grille de solution doit avoir les mêmes dimensions
        self.assertEqual(solution.rows_number, grid.rows_number)
        self.assertEqual(solution.columns_number, grid.columns_number)

if __name__ == '__main__':
    unittest.main()
