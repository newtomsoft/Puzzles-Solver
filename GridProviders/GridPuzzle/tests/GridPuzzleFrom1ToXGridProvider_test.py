import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleFrom1ToXGridProvider import GridPuzzleFrom1ToXGridProvider

class GridPuzzleFrom1ToXGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        await self.run_scrap_test(GridPuzzleFrom1ToXGridProvider, "from1tox_sample.html", "scrap_grid")

if __name__ == '__main__':
    unittest.main()
