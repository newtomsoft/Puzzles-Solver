import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Clouds.CloudsSolver import CloudsSolver

_ = 0


class CloudsSolverTests(TestCase):
    def test_solution_4x4_2674y(self):
        """https://gridpuzzle.com/clouds/2674y"""
        rows_counts = [0, 3, 3, 3]
        columns_counts = [0, 3, 3, 3]
        expected_grid = Grid([
            [_, _, _, _],
            [_, 1, 1, 1],
            [_, 1, 1, 1],
            [_, 1, 1, 1]
        ])
        game_solver = CloudsSolver(rows_counts, columns_counts)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_2674y(self):
        """https://gridpuzzle.com/clouds/31z6o"""
        rows_counts = [4, 4, 0, 3, 3]
        columns_counts = [2, 2, 2, 4, 4]
        expected_grid = Grid([
            [1, 1, 0, 1, 1],
            [1, 1, 0, 1, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1],
            [0, 0, 1, 1, 1]
        ])
        game_solver = CloudsSolver(rows_counts, columns_counts)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_1nz16(self):
        """https://gridpuzzle.com/clouds/1nz16"""
        rows_counts = [4, 7, 7, 7, 0, 3, 5, 5]
        columns_counts = [6, 6, 4, 7, 3, 6, 3, 3]
        expected_grid = Grid([
            [1, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0],
            [1, 1, 0, 1, 1, 1, 0, 0],
            [1, 1, 0, 1, 1, 1, 0, 0]
        ])
        game_solver = CloudsSolver(rows_counts, columns_counts)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_1y9rk(self):
        """https://gridpuzzle.com/clouds/1y9rk"""
        rows_counts = [2, 8, 8, 2, 2, 5, 5, 0, 3, 3]
        columns_counts = [2, 2, 5, 5, 2, 6, 8, 2, 4, 2]
        expected_grid = Grid([
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 1, 1, 1, 0],
            [0, 0, 1, 1, 0, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0]
        ])
        game_solver = CloudsSolver(rows_counts, columns_counts)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15_2674y(self):
        """https://gridpuzzle.com/clouds/31z6o"""
        rows_counts = [2, 2, 11, 11, 11, 0, 4, 8, 8, 2, 2, 9, 7, 3, 0]
        columns_counts = [6, 6, 2, 8, 6, 6, 6, 5, 5, 3, 0, 6, 9, 9, 3]
        expected_grid = Grid([
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0],
            [1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        game_solver = CloudsSolver(rows_counts, columns_counts)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
