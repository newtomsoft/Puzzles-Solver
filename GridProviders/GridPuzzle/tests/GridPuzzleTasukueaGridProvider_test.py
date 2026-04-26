import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleTasukueaGridProvider import GridPuzzleTasukueaGridProvider

class GridPuzzleTasukueaGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        await self.run_scrap_test(GridPuzzleTasukueaGridProvider, "tasukuea_sample.html", "scrap_grid")

if __name__ == '__main__':
    unittest.main()
