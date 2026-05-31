import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleFactorismGridProvider import GridPuzzleFactorismGridProvider

_ = None

class GridPuzzleFactorismGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        grid = await self.run_scrap_test(GridPuzzleFactorismGridProvider, "factorism_sample.html", "scrap_grid")
        expected_grid = Grid([
            [12, _, 8, _],
            [_, _, _, 2],
            [3, _, _, _],
            [_, 12, _, 3]
        ])
        self.assertEqual(expected_grid, grid)


if __name__ == '__main__':
    unittest.main()
