import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleSutoretoGridProvider import GridPuzzleSutoretoGridProvider
from Domain.Puzzles.Sutoreto.SutoretoSolver import SutoretoSolver

_ = 0
x = True
o = False

class GridPuzzleSutoretoGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        provided = await self.run_scrap_test(GridPuzzleSutoretoGridProvider, "sutoreto_sample.html", "scrap_grid")
        expected_grid = Grid([
            [1, _, _, _],
            [_, 5, _, 3],
            [_, _, 2, 1],
            [3, _, 1, _]
        ])
        expected_blacked = Grid([
            [o, o, o, o],
            [o, o, o, o],
            [o, o, o, o],
            [o, o, o, x]
,        ])
        self.assertEqual((expected_grid, expected_blacked), provided)


if __name__ == '__main__':
    unittest.main()
