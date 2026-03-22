import unittest

from Domain.Board.Grid import Grid
from Domain.Puzzles.Sutoreto.SutoretoSolver import SutoretoSolver

B = SutoretoSolver.Black
_ = None

class SutoretoSolverTests(unittest.TestCase):
    def test_solve_4x4_easy_3jeeo(self):
        """https://gridpuzzle.com/sutoreto/3jeeo"""
        grid = Grid([
            [1, _, _, _],
            [_, 5, _, 3],
            [_, _, 2, 1],
            [3, _, 1, B]
        ])
        expected_solution = Grid([
            [1, 4, 3, 2],
            [2, 5, 4, 3],
            [4, 3, 2, 1],
            [3, 2, 1, B]
        ])

        solver = SutoretoSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solve_4x4_evil_1n00d(self):
        """https://gridpuzzle.com/sutoreto/1n00d"""
        grid = Grid([
            [_, 4, 2, _],
            [8, _, _, _],
            [_, _, _, _],
            [_, _, _, 5]
        ])
        expected_solution = Grid([
            [5, 4, 2, 3],
            [8, 7, 5, 6],
            [6, 5, 3, 4],
            [7, 6, 4, 5]
        ])

        solver = SutoretoSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solve_10x10_evil_040m2(self):
        """https://gridpuzzle.com/sutoreto/040m2"""
        grid = Grid([
            [_, 3, _, B, _, _, 1, B, 5, B],
            [_, B, _, _, _, _, B, 3, _, 2],
            [2, _, _, _, B, 6, _, _, _, B],
            [_, 2, B, 2, _, _, _, _, B, 2],
            [_, _, _, _, 5, B, _, 2, _, _],
            [B, _, B, 4, _, _, 2, B, _, _],
            [1, B, 4, B, 4, _, B, 5, _, B],
            [_, 4, _, _, B, 2, _, _, 4, _],
            [_, _, B, 5, _, _, _, _, B, 7],
            [B, _, 5, _, _, 6, B, _, 3, B]
        ])
        expected_solution = Grid([
            [1, 3, 2, B, 2, 3, 1, B, 5, B],
            [5, B, 4, 6, 3, 5, B, 3, 4, 2],
            [2, 4, 3, 5, B, 6, 5, 4, 3, B],
            [3, 2, B, 2, 6, 4, 3, 5, B, 2],
            [4, 1, 2, 3, 5, B, 4, 2, 5, 3],
            [B, 3, B, 4, 3, 5, 2, B, 3, 4],
            [1, B, 4, B, 4, 3, B, 5, 6, B],
            [2, 4, 5, 3, B, 2, 5, 3, 4, 6],
            [3, 2, B, 5, 3, 4, 6, 2, B, 7],
            [B, 3, 5, 4, 2, 6, B, 4, 3, B]
        ])

        solver = SutoretoSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
