import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleContextGridProvider import GridPuzzleContextGridProvider

_ = None


class GridPuzzleContextGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        expected = Grid([
            [_, 3, _, 2, _],
            [_, 3, _, _, 2],
            [_, _, _, _, _],
            [7, _, _, 4, _],
            [_, 4, _, 5, _],
        ])
        result = await self.run_scrap_test(GridPuzzleContextGridProvider, 'context_sample.html', 'scrap_grid')
        self.assert_grid_equals(expected, result)


if __name__ == '__main__':
    unittest.main()
