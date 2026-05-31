import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleKanjoGridProvider import GridPuzzleKanjoGridProvider
from PuzzleSolver.Board.Island import Island

class GridPuzzleKanjoGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        grid = await self.run_scrap_test(GridPuzzleKanjoGridProvider, "kanjo_sample.html", "scrap_grid")
        
        self.assertIsNotNone(grid)
        self.assertIsInstance(grid, Grid)

        # Grid from https://gridpuzzle.com/kanjo/5665w (from KanjoSolver_test.py)
        grid_str = (
            ' ·  ·  1  ·  2  · \n'
            ' ·  ┌─ ·  ·  ┌─ · \n'
            ' │  ·  ·  2  ·  2 \n'
            ' 1  ·  2  ·  · ─┘ \n'
            ' ·  │  ·  · ─── · \n'
            ' ·  1  ·  3  ·  · '
        )
        expected_grid = Grid.from_str(grid_str, type(Island))
        self.assertEqual(str(expected_grid), str(grid))

if __name__ == '__main__':
    unittest.main()
