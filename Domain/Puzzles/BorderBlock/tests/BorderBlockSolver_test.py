import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.BorderBlock.BorderBlockSolver import BorderBlockSolver

_ = BorderBlockSolver.empty


class BorderBlockSolverTests(TestCase):
    def test_multiple_solution(self):
        grid = Grid([
            [1, _, 2],
            [_, _, _],
            [_, _, _],
        ])
        dots_positions = [Position(-0.5, 0.5), Position(2.5, 0.5), ]

        game_solver = BorderBlockSolver(grid, dots_positions)
        self.assertNotEqual(Grid.empty(), game_solver.get_solution())
        self.assertNotEqual(Grid.empty(), game_solver.get_other_solution())
        self.assertEqual(Grid.empty(), game_solver.get_other_solution())

    def test_unique_solution(self):
        grid = Grid([
            [1, _, _],
            [_, 2, _],
            [_, _, 3],
        ])
        dots_positions = [
            Position(-0.5, 0.5), Position(0.5, -0.5), Position(2.5, 1.5), Position(1.5, 2.5)
        ]

        expected_grid = Grid([
            [1, 2, 2],
            [2, 2, 2],
            [2, 2, 3]
        ])
        game_solver = BorderBlockSolver(grid, dots_positions)
        self.assertEqual(expected_grid, game_solver.get_solution())
        self.assertEqual(Grid.empty(), game_solver.get_other_solution())

    def test_impossible_configuration(self):
        grid = Grid([
            [1, _, _],
            [1, 2, _],
            [_, _, _],
        ])
        dots_positions = [
            Position(-0.5, 0.5), Position(0.5, -0.5)
        ]

        game_solver = BorderBlockSolver(grid, dots_positions)
        self.assertEqual(Grid.empty(), game_solver.get_solution())

    def test_basic_3x3(self):
        grid = Grid([
            [1, _, _],
            [4, 2, 3],
            [_, _, _],
        ])
        dots_positions = [
            Position(-0.5, 0.5), Position(0.5, -0.5), Position(0.5, 0.5), Position(2.5, 0.5), Position(2.5, 1.5)
        ]

        expected_grid = Grid([
            [1, 3, 3],
            [4, 2, 3],
            [4, 2, 3]
        ])
        game_solver = BorderBlockSolver(grid, dots_positions)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_5x5_easy_37zjk(self):
        """https://gridpuzzle.com/bodaburokku/37zjk"""
        grid = Grid([
            [_, 3, _, 3, _],
            [_, 3, 6, 5, _],
            [7, _, _, _, 1],
            [_, _, 6, _, _],
            [2, _, 4, _, 4]
        ])
        dots_positions = [
            Position(-0.5, 0.5),
            Position(0.5, 2.5), Position(0.5, 4.5),
            Position(1.5, 1.5), Position(1.5, 4.5),
            Position(2.5, -0.5), Position(2.5, 0.5), Position(2.5, 2.5), Position(2.5, 3.5),
            Position(3.5, 1.5), Position(3.5, 4.5),
            Position(4.5, 1.5)
        ]

        expected_grid = Grid([
            [7, 3, 3, 3, 3],
            [7, 3, 6, 5, 5],
            [7, 7, 6, 5, 1],
            [2, 6, 6, 4, 1],
            [2, 2, 4, 4, 4],
        ])
        game_solver = BorderBlockSolver(grid, dots_positions)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_5x5_evil_319d0(self):
        """https://gridpuzzle.com/bodaburokku/319d0"""
        grid = Grid([
            [_, _, _, _, _],
            [_, 5, 1, 4, _],
            [5, _, 1, _, 6],
            [_, 3, _, 3, _],
            [_, _, 2, _, _]
        ])
        dots_positions = [
            Position(-0.5, 2.5),
            Position(0.5, 2.5),
            Position(1.5, 2.5), Position(1.5, 4.5),
            Position(2.5, 1.5), Position(2.5, 2.5), Position(2.5, 3.5), Position(2.5, 4.5),
            Position(3.5, 0.5),
            Position(4.5, 0.5)
        ]

        expected_grid = Grid([
            [5, 5, 5, 4, 4],
            [5, 5, 1, 4, 4],
            [5, 5, 1, 6, 6],
            [5, 3, 3, 3, 2],
            [5, 2, 2, 2, 2],
        ])
        game_solver = BorderBlockSolver(grid, dots_positions)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_8x8_evil_0p608(self):
        """https://gridpuzzle.com/bodaburokku/0p608"""
        grid = Grid([
            [1, _, _, _, _, _, 15, _],
            [_, _, _, 14, _, _, _, _],
            [_, _, _, 5, _, _, 6, _],
            [_, _, 9, _, _, _, _, 2],
            [4, _, _, _, 14, _, 13, _],
            [10, _, _, _, _, _, 16, _],
            [_, 8, 3, _, 13, _, _, 12],
            [11, _, _, _, _, 7, _, _]
        ])
        dots_positions = [
            Position(-0.5, 1.5), Position(-0.5, 3.5), Position(-0.5, 4.5), Position(-0.5, 6.5), Position(1.5, -0.5), Position(1.5, 1.5), Position(1.5, 4.5),
            Position(1.5, 5.5), Position(1.5, 7.5), Position(2.5, 2.5), Position(2.5, 6.5), Position(3.5, -0.5), Position(3.5, 1.5), Position(3.5, 2.5),
            Position(3.5, 6.5), Position(3.5, 7.5), Position(4.5, -0.5), Position(4.5, 0.5), Position(4.5, 3.5), Position(4.5, 4.5), Position(5.5, -0.5),
            Position(5.5, 0.5), Position(5.5, 5.5), Position(5.5, 7.5), Position(6.5, 5.5), Position(6.5, 7.5), Position(7.5, 0.5), Position(7.5, 1.5),
            Position(7.5, 2.5)
        ]

        expected_grid = Grid([
            [1, 1, 5, 5, 14, 15, 15, 6],
            [1, 1, 5, 14, 14, 15, 6, 6],
            [9, 9, 5, 5, 14, 13, 6, 2],
            [9, 9, 9, 14, 14, 13, 13, 2],
            [4, 4, 3, 3, 14, 13, 13, 16],
            [10, 3, 3, 7, 7, 13, 16, 16],
            [11, 8, 3, 7, 13, 13, 12, 12],
            [11, 8, 3, 7, 7, 7, 7, 7],
        ])
        game_solver = BorderBlockSolver(grid, dots_positions)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_10x10_evil_k9724(self):
        """https://gridpuzzle.com/bodaburokku/k9724"""
        grid = Grid([
            [_, _, 16, _, 10, _, _, _, _, _],
            [_, _, _, 2, _, 21, _, _, 6, _],
            [_, _, _, _, _, _, _, _, _, 4],
            [_, _, 7, _, 15, 17, _, 11, _, _],
            [_, 3, _, _, _, _, _, _, _, _],
            [_, _, 9, _, _, _, _, _, _, _],
            [_, _, 5, _, 1, 1, _, _, 12, _],
            [_, _, _, _, _, 1, 13, _, 18, _],
            [14, _, 20, _, 1, _, _, _, _, _],
            [_, _, 8, _, _, _, _, _, _, 19]
        ])
        dots_positions = [
            Position(-0.5, 0.5), Position(-0.5, 2.5), Position(-0.5, 7.5), Position(0.5, 0.5), Position(0.5, 2.5), Position(0.5, 3.5), Position(0.5, 4.5),
            Position(0.5, 6.5), Position(0.5, 9.5), Position(1.5, 3.5), Position(1.5, 6.5), Position(2.5, 1.5), Position(2.5, 3.5), Position(2.5, 5.5),
            Position(2.5, 6.5), Position(2.5, 7.5), Position(2.5, 9.5), Position(3.5, -0.5), Position(3.5, 1.5), Position(3.5, 2.5), Position(3.5, 8.5),
            Position(4.5, 4.5), Position(4.5, 8.5), Position(5.5, -0.5), Position(5.5, 4.5), Position(6.5, 1.5), Position(6.5, 2.5), Position(7.5, 1.5),
            Position(7.5, 2.5), Position(7.5, 6.5), Position(8.5, 2.5), Position(8.5, 6.5), Position(8.5, 8.5), Position(8.5, 9.5), Position(9.5, 0.5),
            Position(9.5, 3.5), Position(9.5, 4.5)
        ]

        expected_grid = Grid([
            [3, 16, 16, 10, 10, 10, 10, 10, 6, 6],
            [3, 2, 2, 2, 15, 21, 21, 6, 6, 4],
            [3, 2, 7, 7, 15, 15, 15, 6, 4, 4],
            [3, 3, 7, 17, 15, 17, 13, 11, 4, 12],
            [9, 3, 9, 17, 17, 17, 13, 11, 11, 12],
            [9, 9, 9, 9, 9, 13, 13, 13, 13, 12],
            [14, 9, 5, 9, 1, 1, 13, 12, 12, 12],
            [14, 14, 5, 1, 1, 1, 13, 12, 18, 12],
            [14, 8, 20, 1, 1, 1, 1, 18, 18, 12],
            [14, 8, 8, 8, 1, 19, 19, 19, 19, 19],
        ])
        # other =
        # 3 16 16 10 10 10 10 10 6 6
        # 3 2 2 2 15 21 21 6 6 4
        # 3 2 7 7 15 15 15 6 4 4
        # 3 3 7 17 15 17 13 11 4 12
        # 9 3 9 17 17 17 13 11 11 12
        # 9 9 9 9 9 13 13 13 13 12
        # 14 9 5 9 1 1 13 12 12 12
        # 14 14 14 1 1 1 13 12 18 12
        # 14 8 20 1 1 1 1 18 18 12
        # 14 8 8 8 1 19 19 19 19 19

        game_solver = BorderBlockSolver(grid, dots_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
