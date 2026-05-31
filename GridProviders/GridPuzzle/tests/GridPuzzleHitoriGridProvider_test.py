import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleHitoriGridProvider import GridPuzzleHitoriGridProvider


class GridPuzzleHitoriGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        expected = Grid([
            [3, 3, 2, 2],
            [1, 4, 1, 2],
            [1, 1, 4, 3],
            [3, 2, 3, 4]
        ])
        result = await self.run_scrap_test(GridPuzzleHitoriGridProvider, 'hitori_sample.html', 'scrap_grid')
        self.assert_grid_equals(expected, result)

if __name__ == '__main__':
    unittest.main()
