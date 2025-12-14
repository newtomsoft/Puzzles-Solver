import unittest

from Domain.Board.Grid import Grid
from Domain.Puzzles.Fobidoshi.FobidoshiSolver import FobidoshiSolver

_ = -1


class FobidoshiSolverLongTests(unittest.TestCase):
    def test_solution_12x12_evil_2d0q8(self):
        """https://gridpuzzle.com/fobidoshi/2d0q8"""
        grid = Grid([
            [_, 1, 1, 1, _, _, 1, 1, 1, _, 1, _],
            [_, _, 1, _, _, 1, 1, _, _, 1, _, 1],
            [_, _, _, _, _, 1, _, 1, 1, _, 1, _],
            [_, _, _, _, 1, _, 1, _, _, 0, _, _],
            [1, _, 1, _, 1, 1, _, 1, 1, _, _, _],
            [_, 1, 1, 0, _, 1, 1, _, 1, 1, _, _],
            [_, _, 1, _, _, 1, 1, 1, 0, 1, _, _],
            [_, _, _, _, _, _, _, 1, 1, _, 1, _],
            [_, 1, 0, 1, _, 1, 1, _, 1, 1, 1, _],
            [_, _, _, _, _, _, _, _, _, _, _, 1],
            [_, _, _, 1, _, _, _, _, 1, _, _, _],
            [1, _, _, _, 1, _, 1, _, _, _, _, _],
        ])
        expected_grid = Grid([
            [0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1],
            [0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
            [1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0],
            [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
            [0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
            [1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0],
            [1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
            [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1]
        ])
        game_solver = FobidoshiSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
