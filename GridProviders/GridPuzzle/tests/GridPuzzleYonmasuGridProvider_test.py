import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleYonmasuGridProvider import GridPuzzleYonmasuGridProvider


class GridPuzzleYonmasuGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        grid = await self.run_scrap_test(GridPuzzleYonmasuGridProvider, "yonmasu_sample.html", "scrap_grid")
        expected_grid = Grid([
            ['.', '#', '.', '.', '#'],
            ['O', 'O', '.', '.', '.'],
            ['.', '.', '#', '.', '.'],
            ['O', '.', 'O', '.', 'O'],
            ['#', '.', '.', '#', '.'],
        ])
        self.assert_grid_equals(expected_grid, grid)


if __name__ == '__main__':
    unittest.main()
