import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Meadows.MeadowsSolver import MeadowsSolver

_ = MeadowsSolver.empty


class MeadowsSolverTests(TestCase):
    def test_solution_initial_contraints(self):
        grid = Grid([
            [1, 1, 2],
            [1, 1, 3],
            [4, 5, 6],
        ])

        game_solver = MeadowsSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 2],
            [1, 1, 3],
            [4, 5, 6],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_squares2x2_contraints(self):
        grid = Grid([
            [1, _, 2],
            [_, _, 3],
            [4, 5, 6],
        ])

        game_solver = MeadowsSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 2],
            [1, 1, 3],
            [4, 5, 6],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_3w762(self):
        """https://gridpuzzle.com/meadows/3w762"""
        grid = Grid([
            [1, _, _, _, 2, _],
            [_, _, _, 3, _, _],
            [_, _, 4, 5, _, _],
            [_, 6, _, _, 7, _],
            [_, _, _, 8, _, _],
            [_, 9, 10, 11, _, 12],
        ])

        game_solver = MeadowsSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 3, 3, 2, 2],
            [1, 1, 3, 3, 2, 2],
            [6, 6, 4, 5, 7, 7],
            [6, 6, 8, 8, 7, 7],
            [9, 9, 8, 8, 12, 12],
            [9, 9, 10, 11, 12, 12],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_g4kvm(self):
        """https://gridpuzzle.com/meadows/g4kvm"""
        grid = Grid([
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, 1, _, _, _, 2],
            [_, 3, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, 4, 5, _, _, 6, _, _, _, _],
            [_, _, _, 7, _, _, 8, _, _, _],
            [_, 9, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, 10, _, _, _, 11, _, _, 12, _],
            [_, _, _, 13, _, _, _, 14, _, _],
        ])

        game_solver = MeadowsSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [3, 3, 3, 1, 1, 1, 2, 2, 2, 2],
            [3, 3, 3, 1, 1, 1, 2, 2, 2, 2],
            [3, 3, 3, 1, 1, 1, 2, 2, 2, 2],
            [4, 4, 5, 5, 6, 6, 2, 2, 2, 2],
            [4, 4, 5, 5, 6, 6, 8, 8, 8, 8],
            [9, 9, 9, 7, 7, 7, 8, 8, 8, 8],
            [9, 9, 9, 7, 7, 7, 8, 8, 8, 8],
            [9, 9, 9, 7, 7, 7, 8, 8, 8, 8],
            [10, 10, 13, 13, 11, 11, 14, 14, 12, 12],
            [10, 10, 13, 13, 11, 11, 14, 14, 12, 12],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15_5k7xr(self):
        """https://gridpuzzle.com/meadows/5k7xr"""
        grid = Grid([
            [ 1,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  2,  _,  _],
            [ _,  _,  _,  _,  _,  3,  _,  _,  _,  _,  _,  _,  _,  4,  _],
            [ 5,  6,  _,  _,  7,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _],
            [ _,  _,  _,  _,  8,  _,  _,  _,  _,  _,  _,  _,  _,  _,  9],
            [ _,  _,  _,  _,  _,  _,  _,  _, 10,  _,  _,  _,  _,  _,  _],
            [ _,  _,  _,  _,  _, 11, 12,  _,  _,  _, 13,  _,  _,  _,  _],
            [ _,  _, 14,  _, 15,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _],
            [ _,  _,  _, 16,  _,  _,  _,  _, 17,  _,  _,  _,  _,  _,  _],
            [18,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _],
            [ _,  _,  _,  _,  _, 19,  _, 20,  _,  _,  _,  _,  _,  _,  _],
            [21,  _,  _,  _,  _,  _,  _,  _,  _, 22,  _,  _,  _,  _,  _],
            [ _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 23,  _],
            [ _,  _,  _,  _,  _,  _,  _,  _, 24,  _,  _,  _,  _,  _,  _],
            [ _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _,  _, 25, 26,  _],
            [ _,  _, 27,  _, 28, 29,  _,  _,  _,  _,  _,  _,  _,  _,  _],
        ])

        game_solver = MeadowsSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [ 1 , 1,  7,  7,  7,  3,  3,  3,  3,  2,  2,  2,  2,  4,  4],
            [ 1 , 1,  7,  7,  7,  3,  3,  3,  3,  2,  2,  2,  2,  4,  4],
            [ 5 , 6,  7,  7,  7,  3,  3,  3,  3,  2,  2,  2,  2,  9,  9],
            [14, 14, 14, 14,  8,  3,  3,  3,  3,  2,  2,  2,  2,  9,  9],
            [14, 14, 14, 14, 11, 11, 12, 12, 10, 10, 13, 13, 13, 13, 13],
            [14, 14, 14, 14, 11, 11, 12, 12, 10, 10, 13, 13, 13, 13, 13],
            [14, 14, 14, 14, 15, 15, 15, 17, 17, 17, 13, 13, 13, 13, 13],
            [18, 18, 16, 16, 15, 15, 15, 17, 17, 17, 13, 13, 13, 13, 13],
            [18, 18, 16, 16, 15, 15, 15, 17, 17, 17, 13, 13, 13, 13, 13],
            [21, 21, 21, 19, 19, 19, 19, 20, 20, 22, 22, 23, 23, 23, 23],
            [21, 21, 21, 19, 19, 19, 19, 20, 20, 22, 22, 23, 23, 23, 23],
            [21, 21, 21, 19, 19, 19, 19, 24, 24, 24, 24, 23, 23, 23, 23],
            [27, 27, 27, 19, 19, 19, 19, 24, 24, 24, 24, 23, 23, 23, 23],
            [27, 27, 27, 28, 28, 29, 29, 24, 24, 24, 24, 25, 25, 26, 26],
            [27, 27, 27, 28, 28, 29, 29, 24, 24, 24, 24, 25, 25, 26, 26],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
