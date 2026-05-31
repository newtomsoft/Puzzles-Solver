import unittest

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from PuzzleSolver.Puzzles.Araf.ArafSolver import ArafSolver

_ = ArafSolver.empty


class ArafSolverTests(unittest.TestCase):
    def test_araf_5x5_easy_37vej(self):
        """https://gridpuzzle.com/araf/37vej"""
        grid = Grid([
            [_, _, 9, _, 4],
            [_, 2, 7, _, _],
            [_, 2, _, 4, _],
            [_, _, _, 8, 6],
            [_, 7, _, _, 6],
        ])
        solver = ArafSolver(grid)
        solution = solver.get_solution()
        regions_grid = RegionsGrid(solution.matrix)
        expected = (
            "┌─────────┐\n"
            "├─────┬───┤\n"
            "├───┬─┤   │\n"
            "│ ┌─┘ └─┐ │\n"
            "│ └─┐   └─┤\n"
            "└───┴─────┘\n"
        )
        self.assertEqual(str(regions_grid), expected)

    def test_araf_5x5_evil_31x8k(self):
        """https://gridpuzzle.com/araf/31x8k"""
        grid = Grid([
            [_, _, 25, _, 2],
            [_, _, _, 4, 3],
            [_, 7, _, 4, 1],
            [_, 18, _, _, _],
            [6, 7, _, _, _],
        ])
        solver = ArafSolver(grid)
        solution = solver.get_solution()
        regions_grid = RegionsGrid(solution.matrix)
        expected = (
            "┌─────┬───┐\n"
            "│ ┌───┤ ┌─┤\n"
            "│ │   └─┤ │\n"
            "│ ├─────┴─┤\n"
            "│ │       │\n"
            "└─┴───────┘\n"
        )
        self.assertEqual(str(regions_grid), expected)

    def test_araf_16166_6x6_evil(self):
        """https://gridpuzzle.com/araf/16166"""
        grid = Grid([
            [_, _, _, _, _, _],
            [_, _, 2, 10, _, 8],
            [_, _, 5, _, 6, 21],
            [_, 6, _, 6, _, _],
            [_, _, _, 4, _, 13],
            [7, _, _, _, _, 4],
        ])

        solver = ArafSolver(grid)
        solution = solver.get_solution()
        self.assertFalse(solution.is_empty())


if __name__ == '__main__':
    unittest.main()
