import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleDoppelblockGridProvider import GridPuzzleDoppelblockGridProvider

class GridPuzzleDoppelblockGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        await self.run_scrap_test(GridPuzzleDoppelblockGridProvider, "doppelblock_sample.html", "scrap_grid")

if __name__ == '__main__':
    unittest.main()
