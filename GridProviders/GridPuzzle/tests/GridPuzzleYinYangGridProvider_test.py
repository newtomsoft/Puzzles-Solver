from GridProviders.GridPuzzle.GridPuzzleYinYangGridProvider import GridPuzzleYinYangGridProvider
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid


class GridPuzzleYinYangGridProviderTest(GridPuzzleProviderTestBase):
    async def test_scrap_grid(self):
        result = await self.run_scrap_test(GridPuzzleYinYangGridProvider, 'yinyang_sample.html')

        expected_matrix = [
            [None, 0, None, 1],
            [None, None, 1, None],
            [None, None, None, None],
            [None, None, None, 0]
        ]

        expected_grid = Grid(expected_matrix)
        self.assert_grid_equals(expected_grid, result)
