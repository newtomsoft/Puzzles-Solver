import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Moonsun.MoonsunSolver import MoonsunSolver

_ = None
B = MoonsunSolver.black
W = MoonsunSolver.white


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
            ' ┌─────┐ \n'
            ' └──┐  │ \n'
            ' ·  └──┘ '
        )

        game_solver = MoonsunSolver(circle_grid, regions_grid)
        solution = game_solver.solve()
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
            ' ┌─────┐  · \n'
            ' └──┐  │  · \n'
            ' ·  │  │  · \n'
            ' ·  └──┘  · '
        )

        game_solver = MoonsunSolver(circle_grid, regions_grid)
        solution = game_solver.solve()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_5x5_evil_37p94(self):
        """https://gridpuzzle.com/moonsun/37p94"""
        regions_grid = Grid([
            [1, 1, 1, 2, 3],
            [1, 1, 2, 2, 3],
            [1, 4, 4, 5, 6],
            [1, 1, 4, 7, 6],
            [1, 4, 4, 8, 6],
        ])
        circle_grid = Grid([
            [_, W, _, B, B],
            [W, W, _, _, W],
            [_, W, _, W, _],
            [W, _, _, B, B],
            [B, B, _, W, _]
        ])

        expected_solution_str = (
            ' ·  ┌─────┐  · \n'
            ' ┌──┘  ·  └──┐ \n'
            ' │  ·  ┌──┐  │ \n'
            ' └──┐  │  │  │ \n'
            ' ·  └──┘  └──┘ '
        )

        game_solver = MoonsunSolver(circle_grid, regions_grid)
        solution = game_solver.solve()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_12x12_evil_22418(self):
        """https://gridpuzzle.com/moonsun/22418"""
        regions_grid = Grid([
            [1, 1, 1, 2, 2, 3, 4, 4, 5, 5, 5, 5],
            [1, 6, 1, 2, 2, 4, 4, 4, 5, 7, 7, 8],
            [9, 6, 10, 10, 11, 11, 4, 12, 13, 13, 8, 8],
            [9, 6, 10, 10, 14, 11, 14, 12, 15, 15, 16, 16],
            [9, 9, 10, 14, 14, 14, 14, 12, 12, 12, 16, 16],
            [9, 9, 10, 14, 17, 18, 18, 18, 19, 19, 16, 20],
            [21, 21, 22, 22, 17, 18, 18, 18, 19, 20, 16, 20],
            [23, 21, 24, 25, 17, 18, 18, 18, 19, 20, 20, 20],
            [23, 26, 24, 25, 25, 18, 18, 27, 19, 19, 28, 20],
            [29, 29, 30, 30, 31, 31, 32, 27, 27, 19, 28, 28],
            [33, 33, 30, 30, 30, 31, 32, 34, 34, 19, 28, 28],
            [33, 35, 35, 30, 30, 36, 36, 36, 34, 28, 28, 28]
        ])
        circle_grid = Grid([
            [W, _, _, W, B, W, _, B, _, _, B, W],
            [_, _, _, _, _, _, _, _, _, _, W, B],
            [B, _, _, B, W, W, B, _, W, W, W, _],
            [_, B, _, B, _, _, B, W, _, B, W, _],
            [W, B, B, _, _, B, _, W, W, W, _, B],
            [_, _, _, B, _, B, _, W, B, _, _, B],
            [B, _, _, W, W, _, W, _, W, _, _, _],
            [W, _, B, B, W, _, B, _, _, B, B, B],
            [_, W, B, _, W, W, _, _, W, _, W, _],
            [_, B, B, W, _, B, B, B, W, _, _, B],
            [W, W, _, _, _, _, _, _, _, _, _, _],
            [W, B, _, _, W, _, W, B, W, _, _, W]
        ])

        expected_solution_str = (
            ' ┌─────┐  ·  ┌────────┐  ┌─────┐  · \n'
            ' └──┐  └─────┘  ·  ┌──┘  │  ·  └──┐ \n'
            ' ·  │  ·  ┌─────┐  └──┐  └──┐  ·  │ \n'
            ' ┌──┘  ┌──┘  ·  └──┐  │  ·  │  ┌──┘ \n'
            ' │  ·  │  ┌────────┘  └─────┘  │  · \n'
            ' └─────┘  └──┐  ·  ┌──┐  ·  ·  └──┐ \n'
            ' ┌──┐  ┌──┐  │  ┌──┘  │  ┌──┐  ·  │ \n'
            ' │  │  │  └──┘  │  ·  │  │  └─────┘ \n'
            ' │  └──┘  ·  ·  └──┐  │  └──┐  ·  · \n'
            ' └──┐  ·  ┌─────┐  │  │  ·  └─────┐ \n'
            ' ┌──┘  ·  └──┐  │  │  └──┐  ·  ┌──┘ \n'
            ' └───────────┘  └──┘  ·  └─────┘  · '
        )

        game_solver = MoonsunSolver(circle_grid, regions_grid)
        solution = game_solver.solve()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
