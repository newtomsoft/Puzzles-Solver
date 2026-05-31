import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleMirukutiGridProvider import GridPuzzleMirukutiGridProvider

class GridPuzzleMirukutiGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        await self.run_scrap_test(GridPuzzleMirukutiGridProvider, "mirukuti_sample.html", "scrap_grid")

if __name__ == '__main__':
    unittest.main()
