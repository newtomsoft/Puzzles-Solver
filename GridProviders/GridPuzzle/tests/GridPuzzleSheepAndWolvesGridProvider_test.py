import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleSheepAndWolvesGridProvider import GridPuzzleSheepAndWolvesGridProvider

class GridPuzzleSheepAndWolvesGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            ['SheepAndWolvesSolver.S', 'SheepAndWolvesSolver.W', 'SheepAndWolvesSolver.S', '.', 3],
            ['SheepAndWolvesSolver.S', 'SheepAndWolvesSolver.S', 'SheepAndWolvesSolver.S', 3, 'SheepAndWolvesSolver.W'],
            ['.', 1, '.', 1, '.'],
            ['SheepAndWolvesSolver.W', 1, 1, 1, 2],
            ['SheepAndWolvesSolver.S', 2, '.', 3, '.']
        ])
        grid = await self.run_scrap_test(GridPuzzleSheepAndWolvesGridProvider, "sheepandwolves_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
