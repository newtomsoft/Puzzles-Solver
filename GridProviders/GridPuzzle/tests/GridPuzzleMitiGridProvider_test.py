import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleMitiGridProvider import GridPuzzleMitiGridProvider

class GridPuzzleMitiGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        await self.run_scrap_test(GridPuzzleMitiGridProvider, "miti_sample.html", "scrap_grid")

if __name__ == '__main__':
    unittest.main()
