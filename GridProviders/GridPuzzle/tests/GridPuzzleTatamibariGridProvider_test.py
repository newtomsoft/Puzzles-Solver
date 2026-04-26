import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleTatamibariGridProvider import GridPuzzleTatamibariGridProvider

class GridPuzzleTatamibariGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        grid = await self.run_scrap_test(GridPuzzleTatamibariGridProvider, "tatamibari_sample.html", "scrap_grid")
        
        self.assertIsNotNone(grid)
        self.assertIsInstance(grid, Grid)

        # Grid from https://gridpuzzle.com/tatamibari/6m7ev
        # Re-check assets/tatamibari_sample.html content for consistency with Solver test
        expected_matrix = [
            ['|', '.', '-', '.'],
            ['.', '+', '.', '|'],
            ['.', '+', '|', '+'],
            ['-', '.', '.', '.']
        ]
        self.assertEqual(Grid(expected_matrix), grid)

if __name__ == '__main__':
    unittest.main()
