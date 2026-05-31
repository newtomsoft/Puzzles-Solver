from GridProviders.GridPuzzle.GridPuzzleNuribouGridProvider import GridPuzzleNuribouGridProvider
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid


class GridPuzzleNuribouGridProviderTest(GridPuzzleProviderTestBase):
    async def test_scrap_grid(self):
        result = await self.run_scrap_test(GridPuzzleNuribouGridProvider, 'nuribou_sample.html')
        
        expected_matrix = [
            [1, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, 2]
        ]
        
        expected_grid = Grid(expected_matrix)
        self.assert_grid_equals(expected_grid, result)
