import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleTentsGridProvider import GridPuzzleTentsGridProvider

_ = 0
T = GridPuzzleTentsGridProvider.tree_value


class GridPuzzleTentsGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        expected_matrix = [
            [T, _, T, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [T, T, _, _, T],
            [_, _, _, T, _],
        ]
        expected_grid = Grid(expected_matrix)
        expected_tents_numbers_by_column_row = {'column': [2, 0, 1, 1, 2], 'row': [1, 1, 1, 1, 2]}

        grid, tents_numbers_by_column_row = await self.run_scrap_test(GridPuzzleTentsGridProvider, "tents_sample.html", "scrap_grid")

        self.assert_grid_equals(expected_grid, grid)
        self.assertEqual(tents_numbers_by_column_row['column'], expected_tents_numbers_by_column_row['column'])
        self.assertEqual(tents_numbers_by_column_row['row'], expected_tents_numbers_by_column_row['row'])


if __name__ == '__main__':
    unittest.main()
