import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleKuroshutoGridProvider import GridPuzzleKuroshutoGridProvider

class GridPuzzleKuroshutoGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        grid = await self.run_scrap_test(GridPuzzleKuroshutoGridProvider, "kuroshuto_sample.html", "scrap_grid")
        
        self.assertIsNotNone(grid)
        self.assertIsInstance(grid, Grid)

        # Grid from https://gridpuzzle.com/kuroshuto/21e6d
        expected_matrix = [
            [_, _, _, 1, 4],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, 4],
            [_, _, 2, 1, 2]
        ]
        self.assertEqual(Grid(expected_matrix), grid)

if __name__ == '__main__':
    unittest.main()
