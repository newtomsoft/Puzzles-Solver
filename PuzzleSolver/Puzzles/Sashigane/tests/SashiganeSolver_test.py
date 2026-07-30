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
            [_, _, _, 6],
            [4, _, _, _],
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
        other_sol = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_sol)

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

    def test_get_stats(self):
        grid = Grid([[None] * 6 for _ in range(6)])
        solver = SashiganeSolver(grid)
        solver.get_solution()
        stats = solver.get_stats()
        self.assertIn("num_conflicts", stats)
        self.assertIn("num_branches", stats)
        self.assertIn("wall_time", stats)

if __name__ == '__main__':
    unittest.main()
