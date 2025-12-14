import unittest

from Domain.Board.Grid import Grid
from Domain.Puzzles.Kurodoko.KurodokoSolver import KurodokoSolver

_ = KurodokoSolver.empty


class KurodokoSolverTests(unittest.TestCase):
    def test_solve_5x5(self):
        grid = Grid([
            [_, 3, 7, 3, _],
            [_, _, _, _, _],
            [_, _, 9, _, _],
            [_, _, _, _, _],
            [_, 3, 7, 3, _]
        ])

        expected_solution = Grid([
            [_, 1, 1, 1, _],
            [1, _, 1, _, 1],
            [1, 1, 1, 1, 1],
            [1, _, 1, _, 1],
            [_, 1, 1, 1, _],
        ])

        solver = KurodokoSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_7x7_2747025(self):
        """https://fr.puzzle-kurodoko.com/?specific=1&size=1&specid=2747025"""
        grid = Grid([
            [_, _, _, _, _, _, _],
            [5, 6, 5, _, _, _, 3],
            [_, _, _, _, _, 8, _],
            [_, _, 8, _, 8, _, _],
            [_, 5, _, _, _, _, _],
            [9, _, _, _, 10, 12, 7],
            [_, _, _, _, _, _, _],
        ])

        expected_solution = Grid([
            [1, 1, 1, 1, 1, _, 1],
            [1, 1, 1, 1, _, 1, 1],
            [_, 1, _, 1, 1, 1, _],
            [1, _, 1, 1, 1, 1, 1],
            [1, 1, 1, _, 1, 1, _],
            [1, 1, 1, 1, 1, 1, 1],
            [_, 1, 1, 1, _, 1, _],
        ])

        solver = KurodokoSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)




if __name__ == '__main__':
    unittest.main()
