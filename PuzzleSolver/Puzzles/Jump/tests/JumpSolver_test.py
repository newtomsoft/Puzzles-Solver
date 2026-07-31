from unittest import TestCase

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Jump.JumpSolver import JumpSolver

B = JumpSolver.cell_blocked
_ = JumpSolver.cell_empty

class JumpSolverTests(TestCase):
    def test_6x6_easy(self):
        grid = Grid([
            [B, _, _, 19, _, B],
            [1, _, 13, 22, _, _],
            [_, 7, B, B, 28, _],
            [_, _, B, B, _, 4],
            [_, 25, _, _, 10, _],
            [B, 16, _, _, _, B],
        ])
        expected_solution = Grid([
            [B, 23, 2, 19, 12, B],
            [1, 18, 13, 22, 3, 20],
            [24, 7, B, B, 28, 11],
            [17, 14, B, B, 21, 4],
            [8, 25, 6, 15, 10, 27],
            [B, 16, 9, 26, 5, B],
        ])

        solver = JumpSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_9x9_easy(self):
        grid = Grid([
            [_, _, 31, B, B, B, 1, _, _],
            [_, B, 28, _, B, 7, 4, B, _],
            [13, _, B, 34, _, _, B, _, _],
            [B, _, _, _, 16, B, 10, _, B],
            [B, B, _, B, 49, B, 25, B, B],
            [B, _, _, B, _, _, _, _, B],
            [_, _, B, _, _, _, B, 20, 53],
            [46, B, _, 37, B, _, _, B, 22],
            [43, _, _, B, B, B, _, 52, 19],
        ])
        expected_solution = Grid([
            [29, 14, 31, B, B, B, 1, 8, 5],
            [32, B, 28, 15, B, 7, 4, B, 2],
            [13, 30, B, 34, 11, 26, B, 6, 9],
            [B, 33, 12, 27, 16, B, 10, 3, B],
            [B, B, 35, B, 49, B, 25, B, B],
            [B, 47, 40, B, 36, 17, 50, 23, B],
            [39, 44, B, 48, 41, 24, B, 20, 53],
            [46, B, 42, 37, B, 51, 18, B, 22],
            [43, 38, 45, B, B, B, 21, 52, 19],
        ])

        solver = JumpSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        self.assertTrue(solver.get_other_solution().is_empty())
