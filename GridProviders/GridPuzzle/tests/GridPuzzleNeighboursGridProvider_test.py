import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleNeighboursGridProvider import GridPuzzleNeighboursGridProvider

class GridPuzzleNeighboursGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        _ = None
        expected_grid = Grid([
            ['NeighboursSolver.empty', 'NeighboursSolver.empty', 'NeighboursSolver.empty', 2],
            [2, 3, 3, 'NeighboursSolver.empty'],
            [4, 'NeighboursSolver.empty', 'NeighboursSolver.empty', 4],
            ['NeighboursSolver.empty', 2, 'NeighboursSolver.empty', 2],
        ])
        grid = await self.run_scrap_test(GridPuzzleNeighboursGridProvider, "neighbours_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)

if __name__ == '__main__':
    unittest.main()
