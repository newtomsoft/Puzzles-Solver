import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleUsotatamiGridProvider import GridPuzzleUsotatamiGridProvider

class GridPuzzleUsotatamiGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        grid = await self.run_scrap_test(GridPuzzleUsotatamiGridProvider, "usotatami_sample.html", "scrap_grid")
        
        self.assertIsNotNone(grid)
        self.assertIsInstance(grid, Grid)

        # Grid from https://gridpuzzle.com/usotatami/ov8dz (from UsotatamiSolver_test.py)
        expected_matrix = [
            [_, _, 3, _],
            [_, _, _, 2],
            [1, _, 2, _],
            [_, _, 1, 1]
        ]
        self.assertEqual(Grid(expected_matrix), grid)

if __name__ == '__main__':
    unittest.main()
