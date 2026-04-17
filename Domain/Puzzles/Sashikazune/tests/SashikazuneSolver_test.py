import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Sashikazune.SashikazuneSolver import SashikazuneSolver

_ = None


class SashikazuneSolverTests(TestCase):
    def test_solution_5x5_easy_21n99(self):
        """https://gridpuzzle.com/sashikazune/21n99"""
        grid = Grid([
            [5, 1, _, _, 2],
            [4, 2, _, 2, _],
            [_, 3, _, 2, _],
            [_, 3, _, 1, 2],
            [1, _, _, 2, 3]
        ])
        expected_solution_str = (
            "┌─┬─────┬─┐\n"
            "│ │ ┌───┘ │\n"
            "│ │ ├─────┤\n"
            "│ ├─┴───┐ │\n"
            "│ └───┐ │ │\n"
            "└─────┴─┴─┘\n"
        )

        game_solver = SashikazuneSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(str(solution), expected_solution_str)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solution_5x5_evil_oxp11(self):
        """https://gridpuzzle.com/sashikazune/oxp11"""
        grid = Grid([
            [_, _, 3, _, 1],
            [_, _, _, 3, 2],
            [_, _, _, 2, 3],
            [4, 3, _, 1, 2],
            [_, _, _, _, _]
        ])
        expected_solution_str = (
            "┌─────┬───┐\n"
            "│ ┌───┴─┐ │\n"
            "│ │ ┌─┬─┤ │\n"
            "│ │ │ │ └─┤\n"
            "│ │ │ └───┤\n"
            "└─┴─┴─────┘\n"
        )

        game_solver = SashikazuneSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(str(solution), expected_solution_str)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solution_9x9_evil_1xwrd(self):
        """https://gridpuzzle.com/sashikazune/1xwrd"""
        grid = Grid([
            [_, _, _, _, _, _, _, _, _],
            [3, _, _, _, _, 3, _, _, 2],
            [4, _, _, _, 5, _, _, _, _],
            [_, _, _, _, _, _, 4, _, _],
            [_, _, _, 3, _, _, _, _, 4],
            [_, _, 3, _, _, 3, _, _, _],
            [_, _, 3, _, _, _, _, _, _],
            [_, _, _, _, _, _, 6, 3, _],
            [_, _, _, _, _, _, _, _, _]
        ])
        game_solver = SashikazuneSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_str = (
            "┌─────────────┬───┐\n"
            "├─────┬─────┐ ├─┐ │\n"
            "├─┬─┐ │ ┌─┬─┤ │ │ │\n"
            "│ │ │ │ │ │ │ │ └─┤\n"
            "│ │ └─┴─┤ │ └─┴───┤\n"
            "│ └─────┤ ├─────┬─┤\n"
            "├───────┤ └───┐ │ │\n"
            "│ ┌─────┴─────┤ │ │\n"
            "│ │ ┌─────────┴─┘ │\n"
            "└─┴─┴─────────────┘\n"
        )
        self.assertEqual(str(solution), expected_solution_str)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())


if __name__ == '__main__':
    unittest.main()
