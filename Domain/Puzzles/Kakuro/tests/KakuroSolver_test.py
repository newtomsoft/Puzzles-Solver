import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Kakuro.KakuroSolver import KakuroSolver


class KakuroSolverTests(TestCase):


    def test_solution_grid_size_less_than_3(self):
        grid = Grid([
            [0, 0],
            [0, 0],
        ])
        with self.assertRaises(ValueError) as context:
            KakuroSolver(grid)

        self.assertEqual("The grid must be at least 3x3", str(context.exception))

    def test_solution_impossible_sum_19_with_2_numbers(self):
        grid = Grid([
            [[0, 0], [0, 19], [0, 19]],
            [[19, 0], 0, 0],
            [[19, 0], 0, 0],
        ])
        game_solver = KakuroSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_impossible_single_number(self):
        grid = Grid([
            [[0, 0], [0, 2], [0, 5]],
            [[3, 0], 0, 0],
            [[4, 0], 0, 0],
        ])
        game_solver = KakuroSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_minimal_grid(self):
        grid = Grid([
            [[0, 0], [0, 4], [0, 6]],
            [[3, 0], 0, 0],
            [[7, 0], 0, 0],
        ])
        expected_solution = Grid([
            [0, 0, 0],
            [0, 1, 2],
            [0, 3, 4],
        ])
        game_solver = KakuroSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_(self):
        grid = Grid([
            [[0, 0], [0, 4], [0, 6], [0, 0], [0, 6], [0, 4]],
            [[3, 0], 0, 0, [7, 0], 0, 0],
            [[7, 0], 0, 0, [3, 0], 0, 0],
            [[0, 0], [0, 4], [0, 6], [0, 0], [0, 6], [0, 4]],
            [[3, 0], 0, 0, [7, 0], 0, 0],
            [[7, 0], 0, 0, [3, 0], 0, 0],
        ])
        expected_solution = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 1, 2, 0, 4, 3],
            [0, 3, 4, 0, 2, 1],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 2, 0, 4, 3],
            [0, 3, 4, 0, 2, 1],
        ])
        game_solver = KakuroSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_2(self):
        grid = Grid([
            [[0, 0], [0, 4], [0, 6], [0, 0], [0, 0], [0, 6], [0, 4]],
            [[3, 0], 0, 0, [0, 0], [7, 0], 0, 0],
            [[7, 0], 0, 0, [0, 0], [3, 0], 0, 0],
            [[0, 0], [0, 4], [0, 6], [0, 0], [0, 0], [0, 6], [0, 4]],
            [[3, 0], 0, 0, [0, 0], [7, 0], 0, 0],
            [[7, 0], 0, 0, [0, 0], [3, 0], 0, 0],
        ])
        expected_solution = Grid([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 1, 2, 0, 0, 4, 3],
            [0, 3, 4, 0, 0, 2, 1],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 1, 2, 0, 0, 4, 3],
            [0, 3, 4, 0, 0, 2, 1],
        ])
        game_solver = KakuroSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_9x9(self):
        grid = Grid([
            [[0, 0], [0, 0], [0, 16], [0, 4], [0, 0], [0, 6], [0, 4], [0, 15], [0, 0], [0, 0], [0, 6], [0, 7]],
            [[0, 0], [7, 7], 0, 0, [9, 0], 0, 0, 0, [0, 0], [4, 16], 0, 0],
            [[7, 0], 0, 0, 0, [7, 5], 0, 0, 0, [6, 3], 0, 0, 0],
            [[3, 0], 0, 0, [4, 16], 0, 0, [16, 8], 0, 0, 0, 0, 0],
            [[10, 0], 0, 0, 0, 0, [10, 15], 0, 0, 0, 0, [0, 15], [0, 0]],
            [[0, 0], [10, 0], 0, 0, [6, 3], 0, 0, 0, [5, 4], 0, 0, [0, 7]],
            [[0, 0], [0, 6], [10, 7], 0, 0, 0, 0, [12, 7], 0, 0, 0, 0],
            [[16, 0], 0, 0, 0, 0, 0, [4, 3], 0, 0, [4, 4], 0, 0],
            [[7, 0], 0, 0, 0, [8, 0], 0, 0, 0, [6, 0], 0, 0, 0],
            [[3, 0], 0, 0, [0, 0], [7, 0], 0, 0, 0, [3, 0], 0, 0, [0, 0]]
        ])
        expected_solution = Grid([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 4, 3, 0, 1, 3, 5, 0, 0, 3, 1],
            [0, 4, 2, 1, 0, 2, 1, 4, 0, 3, 1, 2],
            [0, 2, 1, 0, 1, 3, 0, 3, 1, 6, 2, 4],
            [0, 1, 3, 2, 4, 0, 3, 1, 2, 4, 0, 0],
            [0, 0, 6, 4, 0, 3, 1, 2, 0, 1, 4, 0],
            [0, 0, 0, 3, 1, 2, 4, 0, 1, 2, 5, 4],
            [0, 3, 1, 6, 2, 4, 0, 1, 3, 0, 3, 1],
            [0, 2, 4, 1, 0, 5, 1, 2, 0, 3, 1, 2],
            [0, 1, 2, 0, 0, 1, 2, 4, 0, 1, 2, 0]
        ])
        game_solver = KakuroSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)


if __name__ == '__main__':
    unittest.main()
