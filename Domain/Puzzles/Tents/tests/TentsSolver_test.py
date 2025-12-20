import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Tents.TentsSolver import TentsSolver

_ = 0
T = TentsSolver.tree_value


class TentsSolverTests(TestCase):
    def test_rows_must_be_at_least_5_raises_value_error(self):
        grid = Grid([
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
        ])
        tents_numbers_by_column_row = {'column': [3, 0, 1, 1, 1], 'row': [2, 0, 1, 1]}
        with self.assertRaises(ValueError) as context:
            TentsSolver(grid, tents_numbers_by_column_row)
        self.assertEqual(str(context.exception), "The rows number must be at least 5")

    def test_with_constraint_sum_in_row_column(self):
        grid = Grid([
            [_, _, _, T, _, _],
            [_, T, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [T, _, _, _, _, _],
            [_, _, _, _, T, _],
        ])
        tents_numbers_by_column_row = {'column': [2, 0, 0, 2, 0, 0], 'row': [0, 2, 0, 0, 0, 2]}
        expected_solution = Grid([
            [_, _, _, _, _, _],
            [1, _, _, 1, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [1, _, _, 1, _, _],
        ])
        game_solver = TentsSolver(grid, tents_numbers_by_column_row)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_no_solution_with_constraint_no_adjacents_tents(self):
        grid = Grid([
            [_, T, _, _, _, _],
            [_, _, _, _, _, T],
            [T, _, T, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
        ])
        tents_numbers_by_column_row = {'column': [1, 1, 1, 0, 1, 0], 'row': [0, 4, 0, 0, 0, 0]}

        game_solver = TentsSolver(grid, tents_numbers_by_column_row)
        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_no_solution_with_no_tent_over_tree_constraint(self):
        grid = Grid([
            [_, _, _, _, _, _],
            [_, _, T, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
        ])
        tents_numbers_by_column_row = {'column': [0, 0, 1, 0, 0, 0], 'row': [0, 1, 0, 0, 0, 0]}
        game_solver = TentsSolver(grid, tents_numbers_by_column_row)
        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_add_free_if_no_tent_near_constraint(self):
        grid = Grid([
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
        ])
        tents_numbers_by_column_row = {'column': [0, 0, 0, 1, 0, 0], 'row': [0, 0, 1, 0, 0, 0]}
        game_solver = TentsSolver(grid, tents_numbers_by_column_row)
        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_no_solution_with_one_tent_for_each_tree_constraint(self):
        grid = Grid([
            [_, T, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [T, _, _, _, _, _],
            [_, _, _, _, _, _],
        ])
        tents_numbers_by_column_row = {'column': [1, 0, 0, 0, 0, 0], 'row': [0, 0, 0, 0, 1, 0]}
        game_solver = TentsSolver(grid, tents_numbers_by_column_row)
        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_1(self):
        grid = Grid([
            [_, T, _, _, _, _],
            [_, _, _, T, _, _],
            [T, _, _, _, _, _],
            [_, _, _, _, T, _],
            [T, _, _, _, _, T],
            [_, T, _, _, _, _],
        ])
        tents_numbers_by_column_row = {'column': [3, 0, 1, 1, 1, 1], 'row': [2, 0, 1, 1, 0, 3]}
        expected_solution = Grid([
            [1, _, _, 1, _, _],
            [_, _, _, _, _, _],
            [_, _, _, _, 1, _],
            [1, _, _, _, _, _],
            [_, _, _, _, _, _],
            [1, _, 1, _, _, 1],
        ])
        game_solver = TentsSolver(grid, tents_numbers_by_column_row)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_2(self):
        grid = Grid([
            [_, _, _, T, _, _],
            [T, _, _, _, _, _],
            [_, _, _, _, T, _],
            [_, T, T, _, _, _],
            [_, _, _, _, _, T],
            [_, T, _, _, _, _]
        ])
        tents_numbers_by_column_row = {'column': [2, 1, 1, 1, 1, 1], 'row': [2, 1, 1, 1, 0, 2]}
        expected_solution = Grid([
            [1, _, 1, _, _, _],
            [_, _, _, _, 1, _],
            [_, 1, _, _, _, _],
            [_, _, _, 1, _, _],
            [_, _, _, _, _, _],
            [1, _, _, _, _, 1]
        ])
        game_solver = TentsSolver(grid, tents_numbers_by_column_row)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_1(self):
        grid = Grid([
            [_, _, _, _, _, _, _, T],
            [T, _, _, T, _, _, _, _],
            [_, _, _, _, _, T, _, _],
            [T, T, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, T],
            [T, _, _, _, T, _, _, _],
            [_, _, _, _, _, T, _, _],
            [_, T, _, _, _, _, _, T]
        ])
        tents_numbers_by_column_row = {'column': [3, 1, 1, 2, 0, 2, 1, 2], 'row': [2, 2, 1, 2, 1, 2, 1, 1]}
        expected_solution = Grid([
            [1, _, _, 1, _, _, _, _],
            [_, _, _, _, _, 1, _, 1],
            [1, _, _, _, _, _, _, _],
            [_, _, 1, _, _, _, _, 1],
            [1, _, _, _, _, _, _, _],
            [_, _, _, 1, _, 1, _, _],
            [_, 1, _, _, _, _, _, _],
            [_, _, _, _, _, _, 1, _]
        ])
        game_solver = TentsSolver(grid, tents_numbers_by_column_row)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_1(self):
        grid = Grid([
            [_, _, _, _, _, _, _, _, _, _],
            [T, _, T, _, _, T, _, T, _, _],
            [T, T, _, _, T, _, _, _, _, T],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, T, _, T],
            [_, T, _, T, T, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, T, T, _, T, _, _, _, T],
            [_, T, _, _, _, _, _, T, _, _],
            [_, _, _, _, _, _, _, T, _, _]
        ])
        tents_numbers_by_column_row = {'column': [3, 2, 3, 1, 2, 1, 2, 1, 3, 2], 'row': [2, 3, 1, 3, 1, 3, 1, 2, 2, 2]}
        expected_solution = Grid([
            [1, _, 1, _, _, _, _, _, _, _],
            [_, _, _, _, 1, _, 1, _, 1, _],
            [_, _, 1, _, _, _, _, _, _, _],
            [1, _, _, _, _, _, _, 1, _, 1],
            [_, _, _, _, 1, _, _, _, _, _],
            [1, _, 1, _, _, _, _, _, _, 1],
            [_, _, _, _, _, 1, _, _, _, _],
            [_, 1, _, _, _, _, _, _, 1, _],
            [_, _, _, 1, _, _, 1, _, _, _],
            [_, 1, _, _, _, _, _, _, 1, _]
        ])
        game_solver = TentsSolver(grid, tents_numbers_by_column_row)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15(self):
        grid = Grid([
            [_, _, _, _, _, _, _, T, _, T, _, _, _, _, _],
            [_, T, _, T, T, T, _, _, _, _, _, _, _, T, _],
            [_, _, _, T, _, _, T, _, _, _, T, _, _, _, _],
            [T, T, _, _, _, _, _, _, _, _, _, _, _, _, T],
            [_, _, _, T, _, _, _, _, _, T, _, _, T, _, _],
            [T, _, _, T, _, _, _, _, _, T, _, _, _, _, _],
            [_, _, _, _, _, _, T, _, _, _, _, _, _, T, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, T, _, _],
            [T, _, _, _, T, _, _, T, _, _, _, _, _, _, T],
            [_, _, T, _, _, _, T, _, _, T, _, _, _, _, _],
            [_, T, _, _, T, T, _, _, _, _, _, T, _, _, T],
            [_, _, _, _, _, T, _, _, T, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, T, _, _, _, T, _, _, _],
            [_, T, _, T, _, _, _, _, _, T, T, _, _, _, T],
            [_, _, _, _, T, _, _, _, T, _, _, _, _, _, _]
        ])
        tents_numbers_by_column_row = {'column': [5, 1, 5, 0, 6, 1, 5, 2, 4, 3, 2, 4, 1, 3, 3], 'row': [4, 3, 2, 3, 3, 2, 4, 2, 4, 2, 4, 3, 2, 4, 3]}
        expected_solution = Grid([
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0]
        ])
        game_solver = TentsSolver(grid, tents_numbers_by_column_row)
        solution = game_solver.get_other_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
