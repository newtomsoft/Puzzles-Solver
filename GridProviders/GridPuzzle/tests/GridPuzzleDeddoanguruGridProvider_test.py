import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleDeddoanguruGridProvider import GridPuzzleDeddoanguruGridProvider


class GridPuzzleDeddoanguruGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        expected = Grid([
            [-1, 3, 4, -1],
            [-1, -1, -1, -1],
            [-1, -1, -1, -1],
            [-1, 1, 0, -1],
        ])
        result = await self.run_scrap_test(GridPuzzleDeddoanguruGridProvider, 'deddoanguru_sample.html', 'scrap_grid')
        self.assert_grid_equals(expected, result)


if __name__ == '__main__':
    unittest.main()
