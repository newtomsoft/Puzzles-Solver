import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleKuroshiroGridProvider import GridPuzzleKuroshiroGridProvider

class GridPuzzleKuroshiroGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        await self.run_scrap_test(GridPuzzleKuroshiroGridProvider, "kuroshiro_sample.html", "scrap_grid")

if __name__ == '__main__':
    unittest.main()
