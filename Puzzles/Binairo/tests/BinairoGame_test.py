import unittest
from unittest import TestCase

from Grid import Grid
from Puzzles.Binairo.BinairoGame import BinairoGame


class BinairoGameTests(TestCase):
    def test_solution_grid_too_small(self):
        grid = Grid([
            [-1, -1, -1, -1, -1],
            [-1, -1, 0, -1, 0],
            [1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [0, 0, -1, -1, 0],
        ])

        with self.assertRaises(ValueError) as context:
            BinairoGame(grid)
        self.assertEqual("Binairo grid must be at least 6x6", str(context.exception))

    def test_solution_not_even_size_column(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, 0, -1],
            [-1, -1, 0, -1, 0, -1, -1],
            [1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1],
            [0, 0, -1, -1, 0, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1],
        ])
        with self.assertRaises(ValueError) as context:
            BinairoGame(grid)
        self.assertEqual("Binairo grid must have an even number of rows/columns", str(context.exception))

    def test_solution_not_even_size_row(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, 0],
            [-1, -1, 0, -1, 0, -1],
            [1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [0, 0, -1, -1, 0, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        with self.assertRaises(ValueError) as context:
            BinairoGame(grid)
        self.assertEqual("Binairo grid must have an even number of rows/columns", str(context.exception))

    def test_solution_using_only_initial_constraint(self):
        grid = Grid([
            [0, 1, 1, 0, 0, 1],
            [0, 1, 1, 0, 1, 0],
            [1, 0, 0, 1, 1, 0],
            [1, 0, 1, 0, 0, 1],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 1],
        ])
        expected_grid = Grid([
            [0, 1, 1, 0, 0, 1],
            [0, 1, 1, 0, 1, 0],
            [1, 0, 0, 1, 1, 0],
            [1, 0, 1, 0, 0, 1],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 1],
        ])
        game = BinairoGame(grid)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_using_initial_constraint_and_count(self):
        grid = Grid([
            [-1, 1, 1, 0, 0, -1],
            [0, -1, 1, 0, -1, 0],
            [1, 0, -1, -1, 1, 0],
            [1, 0, -1, -1, 0, 1],
            [0, -1, 0, 1, -1, 0],
            [-1, 0, 0, 1, 0, -1],
        ])
        expected_grid = Grid([
            [0, 1, 1, 0, 0, 1],
            [0, 1, 1, 0, 1, 0],
            [1, 0, 0, 1, 1, 0],
            [1, 0, 1, 0, 0, 1],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 1],
        ])
        game = BinairoGame(grid)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_using_initial_constraint_and_count_and_unique_row(self):
        grid = Grid([
            [-1, 1, 1, 0, 0, 1],
            [-1, 1, 1, 0, 0, 1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        expected_grid = Grid.empty()
        game = BinairoGame(grid)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_using_initial_constraint_and_count_and_unique_column(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1],
            [0, 0, -1, -1, -1, -1],
            [1, 1, -1, -1, -1, -1],
            [1, 1, -1, -1, -1, -1],
            [0, 0, -1, -1, -1, -1],
            [1, 1, -1, -1, -1, -1],
        ])
        expected_grid = Grid.empty()
        game = BinairoGame(grid)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_using_initial_constraint_and_count_and_unique(self):
        grid = Grid([
            [1, 0, 1, 0, 1, -1],
            [0, 1, 0, 1, -1, 1],
            [-1, 0, 1, 0, -1, -1],
            [0, 1, -1, -1, 1, -1],
            [1, 0, -1, -1, 0, -1],
            [-1, -1, 0, 1, -1, -1],
        ])
        expected_grid = Grid([
            [1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 1],
            [0, 1, 1, 0, 1, 0],
            [1, 0, 0, 1, 0, 1],
            [0, 1, 0, 1, 1, 0],
        ])
        game = BinairoGame(grid)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_using_all_constraints_adjacent_row(self):
        grid = Grid([
            [0, 0, 0, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        expected_grid = Grid.empty()
        game = BinairoGame(grid)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_using_all_constraints_adjacent_column(self):
        grid = Grid([
            [0, -1, -1, -1, -1, -1],
            [0, -1, -1, -1, -1, -1],
            [0, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        expected_grid = Grid.empty()
        game = BinairoGame(grid)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_6x6(self):
        grid = Grid([
            [0, -1, 0, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, 0, -1, 0, 0, -1],
            [0, -1, -1, -1, -1, -1],
            [-1, -1, 0, 0, -1, -1],
            [-1, -1, -1, -1, 1, -1],
        ])
        expected_grid = Grid([
            [0, 1, 0, 1, 0, 1],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 1, 0, 0, 1],
            [0, 0, 1, 1, 0, 1],
            [1, 1, 0, 0, 1, 0],
            [1, 0, 1, 0, 1, 0],
        ])
        game = BinairoGame(grid)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_8x8(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, 1, -1],
            [-1, -1, -1, -1, 1, -1, -1, 1],
            [1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, 1, -1, 1, -1, 0],
            [1, -1, -1, -1, -1, -1, -1, -1],
            [1, -1, -1, 0, 0, -1, -1, -1],
            [-1, -1, 0, 0, -1, -1, 0, -1],
        ])
        expected_grid = Grid([
            [1, 0, 1, 1, 0, 0, 1, 0],
            [0, 1, 1, 0, 0, 1, 1, 0],
            [0, 1, 0, 1, 1, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 0, 1],
            [0, 1, 0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 1, 0, 1, 0],
            [1, 0, 1, 0, 0, 1, 0, 1],
            [0, 1, 0, 0, 1, 1, 0, 1],
        ])
        game = BinairoGame(grid)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_10x10(self):
        grid = Grid([
            [0, 0, 1, 0, 1, 0, 1, -1, -1, 1],
            [-1, -1, 0, 1, 0, 1, -1, -1, 1, 0],
            [-1, -1, 1, 0, 1, 0, 0, 1, 0, 1],
            [-1, -1, 0, 1, -1, -1, 1, 0, 1, 0],
            [1, -1, -1, 0, -1, -1, -1, -1, -1, 0],
            [-1, 0, -1, -1, 1, -1, -1, 1, 0, 1],
            [-1, -1, -1, -1, -1, 1, -1, 0, 1, 0],
            [-1, 1, -1, -1, -1, -1, -1, 0, 1, 0],
            [0, -1, -1, -1, -1, -1, -1, 1, 0, 1],
            [-1, -1, -1, -1, 1, -1, -1, -1, -1, 1],
        ])
        expected_grid = Grid([
            [0, 0, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 1, 0, 1, 0, 1, 0, 0, 1, 0],
            [1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
            [0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
            [1, 0, 1, 0, 0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
            [0, 1, 1, 0, 0, 1, 1, 0, 1, 0],
            [1, 1, 0, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 1, 1, 0, 1, 0, 1, 0, 1],
            [0, 1, 0, 1, 1, 0, 1, 0, 0, 1],
        ])
        game = BinairoGame(grid)
        solution = game.get_solution()
        self.assertEqual(expected_grid, solution)


if __name__ == '__main__':
    unittest.main()
