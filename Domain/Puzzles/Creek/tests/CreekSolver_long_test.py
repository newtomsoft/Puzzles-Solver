import unittest

from Domain.Board.Grid import Grid
from Domain.Puzzles.Creek.CreekSolver import CreekSolver

_ = -1
x = 0


class CreekSolverLongTests(unittest.TestCase):
    def test_solution_15x15_evil_0x6zx8(self):
        # https://gridpuzzle.com/creek/0x6zx8
        grid = Grid([
            [_, _, _, 2, _, 1, 1, _, 1, _, 1, 0, _, _, _, _],
            [_, 3, _, _, 1, _, 2, 2, _, _, 2, _, _, 2, _, _],
            [_, _, 2, _, _, _, _, 2, _, 2, _, 3, _, _, 3, _],
            [_, _, _, 1, 2, _, _, 2, _, _, _, 2, _, 1, 2, _],
            [0, _, _, _, _, _, 3, _, _, _, 2, _, _, 1, _, 2],
            [1, 2, _, 3, _, _, _, 2, _, 1, _, _, 1, _, _, _],
            [1, _, 1, _, _, _, _, _, 1, _, 3, 3, _, _, 2, _],
            [_, 2, _, 2, _, _, 3, _, _, 1, _, _, 3, _, _, _],
            [0, _, 1, _, _, _, 2, _, 0, 2, _, 2, _, 1, _, 2],
            [1, _, 2, _, _, 2, _, 2, _, _, _, _, _, _, 2, _],
            [_, 2, _, 2, _, 1, _, _, _, 2, _, 2, _, 3, _, _],
            [_, _, 2, 2, _, _, 2, _, 2, 1, _, _, _, _, 1, _],
            [_, 1, _, _, 2, 2, _, 1, 3, _, 0, 1, _, 0, _, 2],
            [_, _, 1, _, _, 2, 2, 1, _, _, 1, 2, _, _, 3, _],
            [_, _, _, _, 2, _, _, _, _, _, _, _, 1, _, _, 1],
            [0, _, 2, 2, _, 2, _, _, _, _, 2, _, 0, _, _, _],
        ])
        game_solver = CreekSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 1, x, 1, x, 1, x, 1, x, x, x, 1, 1],
            [x, 1, x, x, x, 1, x, 1, x, 1, x, 1, x, 1, 1],
            [x, 1, x, 1, 1, x, x, 1, x, 1, 1, 1, x, x, 1],
            [x, x, x, x, x, x, 1, x, x, 1, x, x, 1, x, 1],
            [x, 1, 1, 1, x, 1, 1, 1, x, x, 1, x, x, x, 1],
            [1, x, x, 1, x, x, x, x, x, 1, 1, x, 1, x, 1],
            [x, 1, x, 1, x, 1, 1, 1, x, x, 1, 1, x, x, 1],
            [x, 1, x, 1, x, x, 1, x, x, 1, 1, 1, 1, x, 1],
            [x, x, x, x, 1, x, 1, x, x, 1, x, x, x, x, 1],
            [1, 1, 1, x, 1, x, 1, x, 1, 1, x, 1, 1, 1, x],
            [x, x, 1, x, x, x, 1, x, x, x, x, 1, 1, x, x],
            [x, 1, x, 1, x, 1, x, 1, 1, x, x, 1, x, x, 1],
            [x, x, x, 1, x, 1, x, x, 1, x, x, x, x, x, 1],
            [x, 1, x, x, x, 1, x, 1, x, x, 1, 1, x, 1, 1],
            [x, 1, 1, 1, 1, 1, x, x, x, 1, 1, x, x, x, x],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
