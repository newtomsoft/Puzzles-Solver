import unittest

from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleBinairoGridProvider import GridPuzzleBinairoGridProvider
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase

_ = None


class GridPuzzleBinairoGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        expected = Grid([
            [0, _, 1, 1],
            [_, _, _, _],
            [_, 0, 1, _],
            [_, _, _, 0],
        ])
        result = await self.run_scrap_test(GridPuzzleBinairoGridProvider, 'binairo_sample.html', 'scrap_grid')
        self.assert_grid_equals(expected, result)


if __name__ == '__main__':
    unittest.main()
