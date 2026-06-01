import unittest
from unittest import TestCase

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Foseruzu.FoseruzuSolver import FoseruzuSolver

_ = FoseruzuSolver.cell_empty

class FoseruzuSolverTests(TestCase):
    def test_4x4_some_no_clue_multiple_solutions(self):
        grid = Grid([
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
            [_, _, _, _],
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

    def test_6x6_evil_16d40(self):
        """https://gridpuzzle.com/foseruzu/16d40"""
        grid = Grid([
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [2, _, 2, 3, _, 1],
            [_, _, _, _, _, _],
            [2, _, 1, 2, _, 3],
            [_, _, _, _, _, _],
        ])

        game_solver = FoseruzuSolver(grid)
        solution = game_solver.get_solution()
        self.assertFalse(solution.is_empty())
        self.assertTrue(game_solver.get_other_solution().is_empty())

    def test_8x8_evil_0pm0w(self):
        """https://gridpuzzle.com/foseruzu/0pm0w"""
        grid = Grid([
            [_, _, _, _, _, _, _, _],
            [1, _, _, _, 1, _, _, 2],
            [_, 3, _, _, _, _, _, _],
            [3, _, 2, _, _, 2, _, _],
            [_, _, _, _, _, 2, _, _],
            [_, _, _, _, 2, _, 3, 2],
            [_, 3, _, _, _, _, _, _],
            [_, _, _, 2, 3, 2, _, 2],
        ])

        game_solver = FoseruzuSolver(grid)
        solution = game_solver.get_solution()
        self.assertFalse(solution.is_empty())
        self.assertTrue(game_solver.get_other_solution().is_empty())

    def test_4x4_evil_0x95w(self):
        """https://gridpuzzle.com/foseruzu/0x95w"""
        grid = Grid([
            [3, _, 3, _],
            [_, _, 2, _],
            [_, _, _, _],
            [2, _, _, _],
        ])

        game_solver = FoseruzuSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_str = (
            '┌───┬─┬─┐\n'
            '├─┐ │ │ │\n'
            '│ │ │ │ │\n'
            '│ └─┤ │ │\n'
            '└───┴─┴─┘\n'
        )
        self.assertEqual(expected_solution_str, str(solution))
        self.assertTrue(game_solver.get_other_solution().is_empty())

if __name__ == '__main__':
    unittest.main()
