import unittest

from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleArafGridProvider import GridPuzzleArafGridProvider
from PuzzleSolver.Puzzles.Araf.ArafSolver import ArafSolver
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase

_ = ArafSolver.cell_empty


class GridPuzzleArafGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        expected = Grid([
            [_, _, 9, _, 4],
            [_, 2, 7, _, _],
            [_, 2, _, 4, _],
            [_, _, _, 8, 6],
            [_, 7, _, _, 6],
        ])
        result = await self.run_scrap_test(GridPuzzleArafGridProvider, 'araf_sample.html', 'scrap_grid')
        self.assert_grid_equals(expected, result)


if __name__ == '__main__':
    unittest.main()
