import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleNumberCrossGridProvider import GridPuzzleNumberCrossGridProvider

class GridPuzzleNumberCrossGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        await self.run_scrap_test(GridPuzzleNumberCrossGridProvider, "numbercross_sample.html", "scrap_grid")

if __name__ == '__main__':
    unittest.main()
