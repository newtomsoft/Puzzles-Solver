import unittest

from Domain.Board.RegionsGrid import RegionsGrid
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from GridProviders.GridPuzzle.GridPuzzleKinKonKanGridProvider import GridPuzzleKinKonKanGridProvider

class GridPuzzleKinKonKanGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        regions_grid, indices = await self.run_scrap_test(GridPuzzleKinKonKanGridProvider, "kinkonkan_sample.html")

        regions = regions_grid.matrix

        self.assertEqual(indices['top'], ['D3', 'B1', 'C2', 'C2'])
        self.assertEqual(indices['bottom'], ['', '', '', 'A3'])
        self.assertEqual(indices['left'], ['', '', 'D3', 'A3'])
        self.assertEqual(indices['right'], ['B1', '', '', ''])
        
        regions_grid_expected = RegionsGrid([
            [1, 1, 1, 1],
            [2, 1, 3, 4],
            [2, 5, 6, 7],
            [5, 5, 5, 7]
        ])

        self.assertEqual(regions_grid_expected.matrix, regions)


if __name__ == '__main__':
    unittest.main()
