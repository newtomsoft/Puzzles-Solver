import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleRimotoejjiGridProvider import GridPuzzleRimotoejjiGridProvider


class GridPuzzleRimotoejjiGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        expected = Grid([
            [' ', ' ', ' ', ' ', ' '],
            ['↓', ' ', '←', ' ', '+'],
            ['+', ' ', '↑', ' ', '↑'],
            [' ', ' ', ' ', ' ', ' '],
            ['+', '→', '+', '←', '←'],
        ])
        result = await self.run_scrap_test(GridPuzzleRimotoejjiGridProvider, 'rimotoejji_sample.html', 'scrap_grid')
        self.assert_grid_equals(expected, result)

if __name__ == '__main__':
    unittest.main()
