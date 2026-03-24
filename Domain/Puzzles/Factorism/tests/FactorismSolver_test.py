import unittest

from Domain.Board.Grid import Grid
from Domain.Puzzles.Factorism.FactorismSolver import FactorismSolver

_ = FactorismSolver.Empty

class FactorismSolverTests(unittest.TestCase):
    def test_solve_4x4_evil(self):
        """https://gridpuzzle.com/factorism/evil-4"""
        grid = Grid([
            [12, _, 8, _],
            [_, _, _, 2],
            [3, _, _, _],
            [_, 12, _, 3]
        ])
        expected_solution = Grid([
            [_, 3, 4, 2, 1],
            [4, 12, _, 8, _],
            [2, _, _, _, 2],
            [1, 3, _, _, _],
            [3, _, 12, _, 3]
        ])

        solver = FactorismSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solve_5x5_evil(self):
        """https://gridpuzzle.com/factorism/evil-5"""
        grid = Grid([
            [_, 1, 4, _, _],
            [8, _, _, _, _],
            [10, _, _, _, 15],
            [_, _, _, _, 9],
            [_, _, 8, 10, _]
        ])
        expected_solution = Grid([
            [_, 2, 1, 4, 5, 3],
            [1, _, 1, 4, _, _],
            [4, 8, _, _, _, _],
            [5, 10, _, _, _, 15],
            [3, _, _, _, _, 9],
            [2, _, _, 8, 10, _]
        ])

        solver = FactorismSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
