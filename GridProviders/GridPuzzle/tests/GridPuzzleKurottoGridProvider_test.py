import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleKurottoGridProvider import GridPuzzleKurottoGridProvider
from Domain.Puzzles.Kurotto.KurottoSolver import KurottoSolver

_ = KurottoSolver.white


class GridPuzzleKurottoGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        expected = Grid([
            [None, 3, None, 2, None],
            [None, 3, None, None, 2],
            [None, None, None, None, None],
            [7, None, None, 4, None],
            [None, 4, None, 5, None],
        ])
        result = await self.run_scrap_test(GridPuzzleKurottoGridProvider, 'kurotto_sample.html', 'scrap_grid')
        self.assert_grid_equals(expected, result)


if __name__ == '__main__':
    unittest.main()
