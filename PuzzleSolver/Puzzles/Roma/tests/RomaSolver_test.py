import unittest
from unittest import TestCase

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Roma.RomaSolver import RomaSolver

_ = RomaSolver.cell_empty
G = RomaSolver.Goal


class RomaSolverTests(TestCase):

    def test_solution_3x3_invalid(self):
        clues_grid = Grid([
            ['R', 'L', 'L'],
            ['D', 'D', _],
            [_, _, G],
        ])

        regions_grid = Grid([
            [1, 1, 2],
            [3, 2, 2],
            [3, 4, 5],
        ])

        solver = RomaSolver(clues_grid, regions_grid)
        self.assertEqual(Grid.empty(), solver.get_solution())

    def test_solution_3x3_basic(self):
        clues_grid = Grid([
            ['R', _, 'L'],
            ['D', 'D', _],
            [_, _, G],
        ])

        regions_grid = Grid([
            [1, 1, 2],
            [3, 2, 2],
            [3, 4, 5],
        ])

        expected_solution = Grid([
            ['R', 'D', 'L'],
            ['D', 'D', 'U'],
            ['R', 'R', G],
        ])

        solver = RomaSolver(clues_grid, regions_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())


if __name__ == '__main__':
    unittest.main()
