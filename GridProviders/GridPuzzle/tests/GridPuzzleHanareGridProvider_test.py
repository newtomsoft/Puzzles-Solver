import unittest

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from PuzzleSolver.Puzzles.Hanare.HanareSolver import HanareSolver
from GridProviders.GridPuzzle.GridPuzzleHanareGridProvider import GridPuzzleHanareGridProvider
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase


class GridPuzzleHanareGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock(self):
        result = await self.run_scrap_test(GridPuzzleHanareGridProvider, 'hanare_sample.html', 'scrap_grid')
        self.assertIsInstance(result, tuple)
        regions_grid, clues_grid = result

        regions_grid_expected = RegionsGrid([
            [1, 2, 2, 3, 3],
            [1, 2, 4, 5, 6],
            [1, 4, 4, 5, 6],
            [7, 7, 7, 5, 6],
            [7, 7, 5, 5, 6],
        ])

        self.assertEqual(regions_grid_expected.matrix, regions_grid.matrix)

        clues_expected = Grid([
            [3, HanareSolver.cell_empty, HanareSolver.cell_empty, 2, HanareSolver.cell_empty],
            [HanareSolver.cell_empty, HanareSolver.cell_empty, HanareSolver.cell_empty, HanareSolver.cell_empty, HanareSolver.cell_empty],
            [HanareSolver.cell_empty, HanareSolver.cell_empty, 3, HanareSolver.cell_empty, 4],
            [HanareSolver.cell_empty, 5, HanareSolver.cell_empty, HanareSolver.cell_empty, HanareSolver.cell_empty],
            [HanareSolver.cell_empty, HanareSolver.cell_empty, HanareSolver.cell_empty, HanareSolver.cell_empty, HanareSolver.cell_empty],
        ])

        self.assertEqual(clues_expected.matrix, clues_grid.matrix)


if __name__ == '__main__':
    unittest.main()
