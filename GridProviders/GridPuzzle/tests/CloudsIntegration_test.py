import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleCloudsGridProvider import GridPuzzleCloudsGridProvider
from Domain.Puzzles.Clouds.CloudsSolver import CloudsSolver

class CloudsIntegrationTests(GridPuzzleProviderTestBase):
    async def test_scrap_and_solve_clouds(self):
        # 1. Utiliser le provider pour scraper la grille à partir d'un fichier HTML local
        # returns sums_v, sums_h
        sums_v, sums_h = await self.run_scrap_test(GridPuzzleCloudsGridProvider, "clouds_sample.html", "scrap_grid")
        
        self.assertIsNotNone(sums_v)
        self.assertIsNotNone(sums_h)

        # 2. Initialiser le solver avec les données scrapées
        solver = CloudsSolver(sums_v, sums_h)
        
        # 3. Obtenir la solution
        solution = solver.get_solution()
        
        # 4. Vérifications
        self.assertIsNotNone(solution)
        self.assertNotEqual(solution, Grid.empty(), "Le solver devrait trouver une solution pour la grille sample.")
        
        # Grid from https://gridpuzzle.com/clouds/2674y
        # rows_counts = [0, 3, 3, 3]
        # columns_counts = [0, 3, 3, 3]
        expected_solution = Grid([
            [0, 0, 0, 0],
            [0, 1, 1, 1],
            [0, 1, 1, 1],
            [0, 1, 1, 1]
        ])
        self.assertEqual(expected_solution, solution)

if __name__ == '__main__':
    unittest.main()
