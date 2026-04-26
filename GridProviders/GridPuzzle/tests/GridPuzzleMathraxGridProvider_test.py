import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleMathraxGridProvider import GridPuzzleMathraxGridProvider

class GridPuzzleMathraxGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        await self.run_scrap_test(GridPuzzleMathraxGridProvider, "mathrax_sample.html", "scrap_grid")

if __name__ == '__main__':
    unittest.main()
