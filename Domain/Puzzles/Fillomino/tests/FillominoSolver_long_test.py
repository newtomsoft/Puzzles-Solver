import unittest

from Domain.Board.Grid import Grid
from Domain.Puzzles.Fillomino.FillominoSolver import FillominoSolver


class FillominoSolverLongTests(unittest.TestCase):
    def test_9x9_evil(self):
        grid = Grid([
            [6, _, _, _, _, 2, _, _, _],
            [6, _, _, 3, _, 9, _, 1, _],
            [2, 2, 3, _, 9, _, 3, 2, _],
            [_, _, 4, 4, _, _, _, _, _],
            [_, 1, 8, 2, _, 1, 4, 6, _],
            [_, _, _, _, _, 9, 2, _, _],
            [_, 8, 8, _, 9, _, 3, 3, 3],
            [_, 4, _, 3, _, 8, _, _, 2],
            [_, _, _, 2, _, _, _, _, 1],
        ])
        expected_solution = Grid([
            [6, 6, 6, 6, 2, 2, 3, 2, 2],
            [6, 6, 3, 3, 9, 9, 3, 1, 6],
            [2, 2, 3, 9, 9, 4, 3, 2, 6],
            [4, 4, 4, 4, 9, 4, 4, 2, 6],
            [8, 1, 8, 2, 9, 1, 4, 6, 6],
            [8, 8, 8, 2, 9, 9, 2, 2, 6],
            [8, 8, 8, 3, 9, 8, 3, 3, 3],
            [4, 4, 3, 3, 8, 8, 8, 2, 2],
            [4, 4, 2, 2, 8, 8, 8, 8, 1]
        ])
        solver = FillominoSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
