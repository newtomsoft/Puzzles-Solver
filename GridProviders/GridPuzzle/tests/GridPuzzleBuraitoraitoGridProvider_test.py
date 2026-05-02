import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleBuraitoraitoGridProvider import GridPuzzleBuraitoraitoGridProvider
from Domain.Puzzles.Buraitoraito.BuraitoraitoSolver import BuraitoraitoSolver


class GridPuzzleBuraitoraitoGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        expected = Grid([
            [4, 0, 0, 0, 0, 4],
            [0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 3, 0, 1, 0],
            [1, 0, 0, 0, 0, 1]
        ])
        result = await self.run_scrap_test(GridPuzzleBuraitoraitoGridProvider, 'buraitoraito_sample.html', 'scrap_grid')
        self.assert_grid_equals(expected, result)

if __name__ == '__main__':
    unittest.main()
