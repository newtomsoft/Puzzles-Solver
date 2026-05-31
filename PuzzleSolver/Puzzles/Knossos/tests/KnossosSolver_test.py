import unittest
from unittest import TestCase

from pygments.formatters import other

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from PuzzleSolver.Puzzles.Knossos.KnossosSolver import KnossosSolver

_ = KnossosSolver.empty


class KnossosSolverTests(TestCase):
    def test_solution_1x1(self):
        grid = Grid([
            [4],
        ])

        solver = KnossosSolver(grid)
        solution = solver.get_solution()

        self.assertFalse(solution.is_empty())
        self.assertEqual(solution.value(0, 0), 0)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_solution_2x2_two_solutions(self):
        """2x2 grid with two 6: two domino partitions possible."""
        grid = Grid([
            [6, _],
            [_, 6],
        ])

        solver = KnossosSolver(grid)
        solution = solver.get_solution()

        self.assertFalse(solution.is_empty())
        self.assertEqual(solution.rows_number, 2)
        self.assertEqual(solution.columns_number, 2)
        other = solver.get_other_solution()
        self.assertFalse(other.is_empty())
        self.assertNotEqual(solution, other)
        third_solution = solver.get_other_solution()
        self.assertTrue(third_solution.is_empty())

    def test_no_solution(self):
        grid = Grid([
            [4, 6],
            [6, 4],
        ])

        solver = KnossosSolver(grid)
        solution = solver.get_solution()

        self.assertTrue(solution.is_empty())

    def test_solution_3x3(self):
        grid = Grid([
            [_, _, _],
            [_, 12, _],
            [_, _, _],
        ])

        expected_solution_str = (
            '┌─────┐\n'
            '│     │\n'
            '│     │\n'
            '└─────┘\n'
        )

        solver = KnossosSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_str, str(RegionsGrid(solution.matrix)))
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solution_5x5_easy_3164k(self):
        """https://gridpuzzle.com/knossos/3164k"""
        grid = Grid([
            [_, _, 6, _, 4],
            [_, 8, 8, _, _],
            [_, 8, 6, 8, _],
            [_, _, _, _, 6],
            [6, 6, _, _, 6],
        ])

        expected_solution_str = (
            "┌─┬───┬─┬─┐\n"
            "│ └─┬─┘ ├─┤\n"
            "├───┼─┬─┘ │\n"
            "├─┐ │ ├───┤\n"
            "│ ├─┴─┼───┤\n"
            "└─┴───┴───┘\n"
        )

        solver = KnossosSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_str, str(RegionsGrid(solution.matrix)))
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solution_6x6_evil_1y77d(self):
        """https://gridpuzzle.com/knossos/1y77d"""
        grid = Grid([
            [_, _, 6, _, _, _],
            [8, 8, 6, _, _, _],
            [_, 10, _, _, _, _],
            [_, _, _, 6, _, _],
            [_, 6, _, 8, _, 14],
            [_, _, _, 12, 8, _],
        ])

        expected_solution_str = (
            "┌───┬───┬───┐\n"
            "├─┐ ├───┤   │\n"
            "│ ├─┴───┴─┐ │\n"
            "│ ├─┬─┬───┤ │\n"
            "├─┤ │ └─┬─┤ │\n"
            "│ └─┴───┤ └─┤\n"
            "└───────┴───┘\n"
        )

        solver = KnossosSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_str, str(RegionsGrid(solution.matrix)))
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solution_8x8_evil_0p5zw(self):
        """https://gridpuzzle.com/knossos/0p5zw"""
        grid = Grid([
            [_, 6, _, _, _, _, 6, 4],
            [_, 8, _, 8, _, _, 8, _],
            [6, 6, _, 6, _, 10, _, 6],
            [8, 8, _, 4, 8, _, _, _],
            [_, 6, _, _, 8, _, _, _],
            [_, _, 6, _, _, 6, _, 6],
            [10, _, _, 8, 6, _, 6, _],
            [6, _, _, _, _, 8, _, _],
        ])

        expected_solution_str = (
            "┌───┬─┬───┬───┬─┐\n"
            "├─┬─┘ │   ├───┴─┤\n"
            "│ ├───┼───┼───┬─┤\n"
            "├─┼───┼─┬─┴─┐ │ │\n"
            "│ ├─┐ ├─┴─┐ │ ├─┤\n"
            "│ │ ├─┴─┐ ├─┴─┤ │\n"
            "├─┴─┴─┬─┼─┴─┬─┴─┤\n"
            "├───┐ │ └─┬─┴───┤\n"
            "└───┴─┴───┴─────┘\n"
        )

        solver = KnossosSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_str, str(RegionsGrid(solution.matrix)))
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solution_9x9_evil__1gyz9(self):
        """https://gridpuzzle.com/knossos/1gyz9"""
        grid = Grid([
            [_, 4, _, 6, _, _, _, 10, 6],
            [8, _, _, _, 8, _, _, 8, _],
            [_, _, 6, 4, 6, _, _, 8, _],
            [8, _, 10, _, _, 8, _, 8, _],
            [_, _, 6, 4, _, _, _, _, _],
            [_, 8, _, _, _, _, _, 6, _],
            [_, _, 6, 10, _, 4, _, 8, 6],
            [_, 8, _, 10, _, 8, _, _, 10],
            [_, 10, _, 8, _, _, _, _, _],
        ])

        expected_solution_str = (
            "┌─┬─┬───┬───────┬─┐\n"
            "│ └─┼───┴─┬─────┤ │\n"
            "├─┬─┴─┬─┬─┴─┬───┴─┤\n"
            "│ └─┬─┴─┴─┬─┴─┬───┤\n"
            "├─┬─┴─┬─┐ │   ├─┐ │\n"
            "│ └─┬─┼─┴─┴─┬─┤ ├─┤\n"
            "├───┤ │ ┌─┬─┤ └─┤ │\n"
            "├─┐ ├─┴─┘ ├─┴───┼─┤\n"
            "│ └─┴─┬───┴─┬───┘ │\n"
            "└─────┴─────┴─────┘\n"
        )

        solver = KnossosSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_str, str(RegionsGrid(solution.matrix)))
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())


if __name__ == '__main__':
    unittest.main()
