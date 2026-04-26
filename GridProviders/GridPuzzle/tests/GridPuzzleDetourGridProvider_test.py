import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleDetourGridProvider import GridPuzzleDetourGridProvider

class GridPuzzleDetourGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        await self.run_scrap_test(GridPuzzleDetourGridProvider, "detour_sample.html", "scrap_grid")

if __name__ == '__main__':
    unittest.main()
