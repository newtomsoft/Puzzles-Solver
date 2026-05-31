import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleArofuroGridProvider import GridPuzzleArofuroGridProvider
from PuzzleSolver.Puzzles.Arofuro.ArofuroSolver import ArofuroSolver

class GridPuzzleArofuroGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        B = 'B'
        grid = await self.run_scrap_test(GridPuzzleArofuroGridProvider, "arofuro_sample.html", "scrap_grid")
        
        self.assertIsNotNone(grid)
        self.assertIsInstance(grid, Grid)

        # Grid from https://gridpuzzle.com/arofuro/375gk
        expected_matrix = [
            [1, _, _, 3],
            [B, _, _, B],
            [_, _, _, _],
            [5, _, _, 1]
        ]
        self.assertEqual(Grid(expected_matrix), grid)

if __name__ == '__main__':
    unittest.main()
