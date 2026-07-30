import unittest
from unittest import TestCase

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Sashigane.SashiganeSolver import SashiganeSolver

_ = None
U = Direction.up()
D = Direction.down()
L = Direction.left()
R = Direction.right()


class SashiganeSolverTests(TestCase):
    def test_4x4_numbered_circles(self):
        grid = Grid([
            [_, _, _, 0],
            [_, _, _, _],
            [_, _, _, _],
            [_, 3, 3, _],
        ])
        expected_solution_str = (
            '┌───────┐\n'
            '├─────┐ │\n'
            '│ ┌─┬─┤ │\n'
            '├─┘ │ └─┤\n'
            '└───┴───┘\n'
        )

        solver = SashiganeSolver(grid)
        sol = solver.get_solution()
        self.assertEqual(expected_solution_str, str(sol))
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_8x8_evil(self):
        """https://gridpuzzle.com/sashigane/2yx4d"""
        grid = Grid([
            [_, _, _, R, _, _, _, 7],
            [_, _, _, _, _, _, _, _],
            [_, _, 0, _, L, _, _, _],
            [_, 7, _, _, _, _, _, _],
            [6, _, _, _, _, _, 6, _],
            [_, _, 0, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [6, _, _, _, 5, _, _, _],
        ])
        expected_solution_str = (
            '┌─┬─┬─┬─────────┐\n'
            '│ │ │ ├─────┬─┐ │\n'
            '│ │ │ └───┐ │ │ │\n'
            '│ │ └─────┤ │ ├─┤\n'
            '│ └─┬─┬─┬─┴─┘ │ │\n'
            '├─┬─┘ │ ├─┬───┘ │\n'
            '│ ├───┘ │ ├─────┤\n'
            '│ └─────┤ └───┐ │\n'
            '└───────┴─────┴─┘\n'
        )

        solver = SashiganeSolver(grid)
        sol = solver.get_solution()
        self.assertEqual(expected_solution_str, str(sol))
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_3x3_no_solution(self):
        grid = Grid([[None] * 3 for _ in range(3)])
        solver = SashiganeSolver(grid)
        sol = solver.get_solution()
        self.assertTrue(sol.is_empty())

    def test_other_solution(self):
        grid = Grid([[None] * 6 for _ in range(6)])
        solver = SashiganeSolver(grid)
        sol1 = solver.get_solution()
        self.assertFalse(sol1.is_empty())
        sol2 = solver.get_other_solution()
        self.assertFalse(sol2.is_empty())
        self.assertNotEqual(str(sol1), str(sol2))


if __name__ == '__main__':
    unittest.main()
