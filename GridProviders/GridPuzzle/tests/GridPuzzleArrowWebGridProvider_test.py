import unittest

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleArrowWebGridProvider import GridPuzzleArrowWebGridProvider
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase


class GridPuzzleArrowWebGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        expected_directions = Grid([
            ['d', 'd', 'ld', 'ld'],
            ['ru', 'r', 'lu', 'ld'],
            ['ru', 'rd', 'r', 'u'],
            ['ru', 'lu', 'r', 'lu'],
        ])
        result = await self.run_scrap_test(GridPuzzleArrowWebGridProvider, 'arrow_web_sample.html', 'scrap_grid')
        self.assert_grid_equals(expected_directions, result)


if __name__ == '__main__':
    unittest.main()
