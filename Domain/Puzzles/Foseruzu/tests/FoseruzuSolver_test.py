import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Foseruzu.FoseruzuSolver import FoseruzuSolver

_ = FoseruzuSolver.cell_empty

class FoseruzuSolverTests(TestCase):
    def test_4x4_with_some_no_clue(self):
        grid = Grid([
            [3, 2, 2, 3],
            [2, _, _, 2],
            [2, _, _, 2],
            [3, 2, 2, 3],
        ])

        game_solver = FoseruzuSolver(grid)
        solution = game_solver.get_solution()
        self.assertFalse(solution.is_empty())
        other_solution = game_solver.get_other_solution()
        self.assertFalse(other_solution.is_empty())
        self.assertNotEqual(solution, other_solution)

    def test_4x4_easy_3794l(self):
        """https://gridpuzzle.com/foseruzu/3794l"""
        grid = Grid([
            [3, 3, 2, 2],
            [2, 3, 3, 3],
            [2, 2, 2, 2],
            [3, 2, 3, 3],
        ])

        game_solver = FoseruzuSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_str = (
            '┌─┬─────┐\n'
            '│ ├─┬─┐ │\n'
            '│ │ │ └─┤\n'
            '│ │ └─┐ │\n'
            '└─┴───┴─┘\n'
        )
        self.assertEqual(expected_solution_str, str(solution))
        self.assertTrue(game_solver.get_other_solution().is_empty())


    def test_4x4_evil_3794l(self):
        """https://gridpuzzle.com/foseruzu/3794l"""
        grid = Grid([
            [3, 3, 2, 2],
            [2, 3, 3, 3],
            [2, 2, 2, 2],
            [3, 2, 3, 3],
        ])

        game_solver = FoseruzuSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_str = (
            ''
        )
        self.assertEqual(expected_solution_str, str(solution))
        self.assertTrue(game_solver.get_other_solution().is_empty())

if __name__ == '__main__':
    unittest.main()
