import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleKnossosGridProvider import GridPuzzleKnossosGridProvider
from Domain.Puzzles.Knossos.KnossosSolver import KnossosSolver

_ = KnossosSolver.empty


class GridPuzzleKnossosGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        expected = Grid([
            [_, _, 6, _, 4],
            [_, 8, 8, _, _],
            [_, 8, 6, 8, _],
            [_, _, _, _, 6],
            [6, 6, _, _, 6],
        ])
        result = await self.run_scrap_test(GridPuzzleKnossosGridProvider, 'knossos_3164k.html', 'scrap_grid')
        self.assert_grid_equals(expected, result)

    async def test_scrap_grid_1gyz9(self):
        expected = Grid([
            [_, 4, _, 6, _, _, _, 10, 6],
            [8, _, _, _, 8, _, _, 8, _],
            [_, _, 6, 4, 6, _, _, 8, _],
            [8, _, 10, _, _, 8, _, 8, _],
            [_, _, 6, 4, _, _, _, _, _],
            [_, 8, _, _, _, _, _, 6, _],
            [_, _, 6, 10, _, 4, _, 8, 6],
            [_, 8, _, 10, _, 8, _, _, 10],
            [_, 10, _, 8, _, _, _, _, _],
        ])
        result = await self.run_scrap_test(GridPuzzleKnossosGridProvider, 'knossos_1gyz9.html', 'scrap_grid')
        self.assert_grid_equals(expected, result)


if __name__ == '__main__':
    unittest.main()
