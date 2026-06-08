import unittest
from GridProviders.GridPuzzle.tests.base_test import GridPuzzleProviderTestBase
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleCirclesAndSquaresGridProvider import GridPuzzleCirclesAndSquaresGridProvider
from PuzzleSolver.Puzzles.CirclesAndSquares.CirclesAndSquaresSolver import CirclesAndSquaresSolver

B = CirclesAndSquaresSolver.Black
W = CirclesAndSquaresSolver.White
_ = CirclesAndSquaresSolver.cell_empty

class GridPuzzleCirclesAndSquaresGridProviderTests(GridPuzzleProviderTestBase):
    async def test_scrap_grid_with_mock_3n2qr(self):
        """Test scrap_grid with real content from https://gridpuzzle.com/circles-and-squares/3n2qr (from asset)"""
        expected_grid = Grid([
            [W, B, _, B, W],
            [_, _, _, _, _],
            [W, W, _, B, _],
            [W, W, _, _, B],
            [W, _, W, _, W]
        ])
        grid = await self.run_scrap_test(GridPuzzleCirclesAndSquaresGridProvider, "circlesandsquares_sample.html", "scrap_grid")
        self.assert_grid_equals(expected_grid, grid)


if __name__ == '__main__':
    unittest.main()
