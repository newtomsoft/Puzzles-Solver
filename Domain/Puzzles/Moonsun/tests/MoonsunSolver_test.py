import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Moonsun.MoonsunSolver import MoonsunSolver

_ = None
B = 'b'
W = 'w'


class MoonsunSolverTest(TestCase):
    def test_basic_3x3(self):
        regions_grid = Grid([
            [1, 1, 2],
            [3, 4, 2],
            [3, 4, 4],
        ])
        circle_grid = Grid([
            [B, _, W],
            [W, B, _],
            [_, B, B]
        ])
        expected_solution_str = (
           ' ·  ┌─────┐ \n'
           ' ·  └──┐  │ \n'
           ' ·  ·  └──┘ \n'
           ' ·  ·  ·  · '
        )

        game_solver = MoonsunSolver(circle_grid, regions_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_4x4(self):
        regions_grid = Grid([
            [1, 1, 2, 2],
            [3, 3, 2, 2],
            [3, 4, 5, 6],
            [4, 4, 6, 6],
        ])
        circle_grid = Grid([
            [B, _, W, _],
            [_, W, _, B],
            [_, _, B, _],
            [_, B, W, B]
        ])
        expected_solution_str = (
            ' ·  ┌─────┐ \n'
            ' ·  └──┐  │ \n'
            ' ·  ·  └──┘ \n'
            ' ·  ·  ·  · '
        )

        game_solver = MoonsunSolver(circle_grid, regions_grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
