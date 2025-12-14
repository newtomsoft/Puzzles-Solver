import unittest

from Domain.Board.Grid import Grid
from Domain.Puzzles.Nurikabe.NurikabeSolver import NurikabeSolver


class NurikabeSolverLongTests(unittest.TestCase):
    def test_get_solution_12x(self):  # approx 4,8 seconds
        grid = Grid([
            [0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 2, 0, 3, 0, 1, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 7, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
        ])
        expected_solution = Grid([
            [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
            [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
        ])
        game_solver = NurikabeSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
