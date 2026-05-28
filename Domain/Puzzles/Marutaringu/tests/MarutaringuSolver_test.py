from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Marutaringu.MarutaringuSolver import MarutaringuSolver

_ = 0


class MarutaringuSolverTest(TestCase):
    def test_gridpuzzle_5x5_easy_37rj1(self):
        """https://gridpuzzle.com/marutaringu/37rj1"""
        regions_grid = Grid([
            [0, 1, 1, 1, 1],
            [0, 1, 2, 3, 3],
            [4, 4, 2, 3, 3],
            [4, 4, 2, 5, 6],
            [5, 5, 5, 5, 6],
        ])

        clues_grid = Grid([
            [2, 2, _, _, _],
            [_, _, 2, 2, _],
            [2, _, _, _, _],
            [_, _, _, _, 2],
            [4, _, _, _, _],
        ])

        expected = Grid([
            [1, 1, 1, _, _],
            [1, _, 1, _, _],
            [1, _, 1, 1, 1],
            [1, _, _, _, 1],
            [1, 1, 1, 1, 1],
        ])

        solver = MarutaringuSolver(regions_grid, clues_grid)
        solution = solver.get_solution()
        self.assertEqual(expected, solution)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_gridpuzzle_5x5_evil_3nv5w(self):
        """https://gridpuzzle.com/marutaringu/3nv5w"""
        regions_grid = Grid([
            [0, 0, 1, 1, 1],
            [2, 3, 3, 3, 3],
            [2, 4, 4, 4, 5],
            [6, 6, 6, 6, 5],
            [7, 7, 7, 8, 8],
        ])

        clues_grid = Grid([
            [_, _, 1, _, _],
            [_, _, _, _, _],
            [_, 2, _, _, _],
            [1, _, _, _, _],
            [_, _, _, _, _],
        ])

        expected = Grid([
            [1, 1, 1, _, _],
            [1, _, 1, _, _],
            [1, _, 1, 1, 1],
            [1, _, _, _, 1],
            [1, 1, 1, 1, 1],
        ])

        solver = MarutaringuSolver(regions_grid, clues_grid)
        solution = solver.get_solution()
        self.assertEqual(expected, solution)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_gridpuzzle_10x10_evil_0g9er(self):
        """https://gridpuzzle.com/marutaringu/0g9er"""
        regions_grid = Grid([
            [0, 0, 0, 0, 0, 1, 1, 2, 3, 3],
            [0, 0, 4, 4, 5, 1, 2, 2, 2, 3],
            [6, 7, 7, 4, 5, 1, 8, 8, 2, 9],
            [6, 7, 7, 4, 5, 8, 8, 2, 2, 9],
            [10, 7, 7, 4, 5, 8, 8, 8, 11, 9],
            [10, 7, 12, 12, 12, 13, 14, 11, 11, 9],
            [10, 15, 15, 12, 12, 13, 14, 11, 11, 16],
            [10, 15, 12, 12, 17, 13, 14, 11, 11, 16],
            [18, 15, 15, 15, 17, 13, 14, 14, 19, 19],
            [18, 18, 15, 17, 17, 19, 19, 19, 19, 19],
        ])
        clues_grid = Grid([
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 2, 0, 1, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])

        expected = Grid([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])

        solver = MarutaringuSolver(regions_grid, clues_grid)
        solution = solver.get_solution()
        self.assertEqual(expected, solution)
        self.assertTrue(solver.get_other_solution().is_empty())
