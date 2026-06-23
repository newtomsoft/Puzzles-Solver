import unittest
from unittest import TestCase

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.OneFourTwoSix.OneFourTwoSixSolver import OneFourTwoSixSolver

_ = OneFourTwoSixSolver.cell_empty


class OneFourTwoSixSolverTests(TestCase):
    def test_5x6_unique_solution(self):
        grid = Grid([
            [3, _, 3, _, _, _],
            [_, _, _, 1, _, _],
            [_, 1, _, _, _, _],
            [2, _, _, 2, _, 2],
            [_, _, _, 2, _, _],
            [_, 3, _, _, _, 3]
        ])

        solver = OneFourTwoSixSolver(grid)
        solution = solver.get_solution()
        self.assertFalse(solution.is_empty())


if __name__ == '__main__':
    unittest.main()
