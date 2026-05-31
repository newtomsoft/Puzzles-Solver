import unittest

from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleObitaruGridProvider import GridPuzzleObitaruGridProvider
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase

_ = None
W = 'w'


class GridPuzzleObitaruGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        expected = Grid([
            [_, W, _, _, W],
            [W, _, W, _, _],
            [_, _, _, 2, _],
            [_, _, _, _, _],
            [_, _, W, _, _],
        ])
        result = await self.run_scrap_test(GridPuzzleObitaruGridProvider, 'obitaru_sample.html', 'scrap_grid')
        self.assert_grid_equals(expected, result)

    async def test_scrap_grid_7x7_evil_15770(self):
        expected = Grid([
            [_, W, W, W, W, W, _],
            [W, _, _, W, _, _, W],
            [W, 8, _, W, _, 9, W],
            [W, _, _, W, _, _, W],
            [W, W, W, W, W, W, W],
            [W, W, _, W, _, 10, W],
            [W, W, W, W, W, W, W],
        ])
        result = await self.run_scrap_test(GridPuzzleObitaruGridProvider, 'obitaru_15770.html', 'scrap_grid')
        self.assert_grid_equals(expected, result)

    async def test_scrap_grid_8x8_evil_1g0zk(self):
        expected = Grid([
            [W, _, W, W, _, _, _, _],
            [W, W, W, _, 8, _, W, _],
            [_, W, W, _, W, W, W, W],
            [W, _, W, W, W, _, W, _],
            [W, 16, W, _, _, W, _, _],
            [W, _, W, W, _, W, W, W],
            [W, W, W, W, _, _, W, W],
            [_, _, W, W, W, W, _, _],
        ])
        result = await self.run_scrap_test(GridPuzzleObitaruGridProvider, 'obitaru_1g0zk.html', 'scrap_grid')
        self.assert_grid_equals(expected, result)


if __name__ == '__main__':
    unittest.main()
