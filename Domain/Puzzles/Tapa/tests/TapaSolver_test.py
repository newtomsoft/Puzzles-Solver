import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Tapa.TapaSolver import TapaSolver

_ = 0
X = 1

class TapaSolverTests(TestCase):


    def test_solution_not_grid(self):
        grid = Grid([[1], ])
        with self.assertRaises(ValueError) as context:
            TapaSolver(grid)

        self.assertEqual("The grid must be at least 2x2", str(context.exception))

    def test_solution_grid_without_list_numbers(self):
        grid = Grid([
            [1, 1],
            [_, 1]
        ])
        with self.assertRaises(ValueError) as context:
            TapaSolver(grid)

        self.assertEqual("The grid must contain at least one list number", str(context.exception))

    def test_solution_grid_with_too_small_number(self):
        grid = Grid([
            [[-1], [1]],
            [_, [1]]
        ])
        with self.assertRaises(ValueError) as context:
            game_solver = TapaSolver(grid)

            game_solver.get_solution()
        self.assertEqual("Number must be positive and less than 9", str(context.exception))

    def test_solution_grid_with_too_big_number(self):
        grid = Grid([
            [[9], [1]],
            [_, [1]]
        ])
        with self.assertRaises(ValueError) as context:
            game_solver = TapaSolver(grid)

            game_solver.get_solution()
        self.assertEqual("Number must be positive and less than 9", str(context.exception))

    def test_solution_not_exist_white_on_number(self):
        grid = Grid([
            [[1], [1]],
            [[1], [1]],
        ])

        game_solver = TapaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_not_exist_black_count_around_1_number(self):
        grid = Grid([
            [[4], _],
            [_, _],
        ])

        game_solver = TapaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_exist_basic_grid_1_number(self):
        grid = Grid([
            [[3], _],
            [_, _],
        ])
        expected_solution = Grid([[_, 1], [1, 1]])

        game_solver = TapaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_exist_basic_grid_1_number_8(self):
        grid = Grid([
            [_, _, _],
            [_, [8], _],
            [_, _, _],
        ])
        expected_solution = Grid([
            [X, X, X],
            [X, _, X],
            [X, X, X]
        ])

        game_solver = TapaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_exist_basic_grid_2_numbers(self):
        grid = Grid([
            [[2], _],
            [[2], _],
        ])
        expected_solution = Grid([
            [_, X], 
            [_, X]
        ])

        game_solver = TapaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_not_exist_black_square(self):
        grid = Grid([
            [[1], [2], [2], [1]],
            [[2], _, _, [2]],
            [[2], _, _, [2]],
            [[1], [2], [2], [1]],

        ])
        game_solver = TapaSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_not_exist_black_count_around_2_numbers(self):
        grid = Grid([
            [[3, 1], _],
            [_, _],
        ])
        game_solver = TapaSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_not_exist_black_count_around_2_numbers_without_gap(self):
        grid = Grid([
            [[2, 1], _],
            [_, _],
        ])
        game_solver = TapaSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_exist_grid_with_list_count_1_1(self):
        grid = Grid([
            [[1, 1], _, _],
            [_, [7], _],
            [_, _, _],
        ])
        expected_solution = Grid([
            [_, X, X],
            [X, _, X],
            [X, X, X]
        ])

        game_solver = TapaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_exist_grid_with_list_count_2_2(self):
        grid = Grid([
            [_, _, _, _],
            [_, [7], [2, 2], _],
            [_, _, _, _],
            [[2], _, _, [1]],
        ])
        expected_solution = Grid([
            [X, X, X, _],
            [X, _, _, _],
            [X, X, X, _],
            [_, _, _, _]
        ])

        game_solver = TapaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_not_exist_isolated_black(self):
        grid = Grid([
            [[2], _],
            [_, [2]],
        ])
        game_solver = TapaSolver(grid)

        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_grid_6x6(self):
        grid = Grid([
            [[1, 1], _, _, _, _, [1]],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [_, [7], _, _, [5], _],
            [_, _, [1, 1, 2], [1, 4], _, _],
            [[2], _, _, _, _, [3]],
        ])
        expected_solution = Grid([
            [_, X, X, _, _, _],
            [X, _, X, X, X, _],
            [X, X, X, _, X, X],
            [X, _, X, _, _, X],
            [X, X, _, _, X, X],
            [_, _, X, X, X, _]
        ])

        game_solver = TapaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_grid_10x10(self):
        grid = Grid([
            [[2], _, _, _, _, _, _, _, _, [2]],
            [_, _, _, [6], [1, 3], [1, 3], [2, 2], _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, [3], _, [6], _, _, [2, 3], _, [7], _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, [6], [1, 4], _, _, _, _],
            [_, [3], _, _, _, _, _, _, [3, 3], _],
            [_, [4], _, _, [6], [1, 3], _, _, [2, 4], _],
            [_, _, [1, 2], _, _, _, _, [1, 1, 1], _, _]
        ])
        expected_solution = Grid([
            [_, _, X, X, _, _, X, X, X, _],
            [X, X, X, _, _, _, _, _, X, _],
            [_, _, X, X, X, X, X, _, X, X],
            [_, _, X, _, X, _, _, X, _, X],
            [_, _, X, _, _, _, X, X, X, X],
            [X, X, X, X, X, X, X, _, _, X],
            [X, _, _, X, _, _, X, X, _, X],
            [X, _, _, X, X, _, _, X, _, X],
            [X, _, _, X, _, _, _, X, _, X],
            [X, X, _, X, X, X, X, _, X, X]
        ])

        game_solver = TapaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_grid_10x10_2(self):
        grid = Grid([
            [_, _, _, _, [3], _, _, _, _, _],
            [_, [7], _, _, _, _, _, _, _, _],
            [[1, 1, 1], _, _, _, [6], _, _, _, [3], _],
            [_, [2, 3], _, _, _, _, _, _, [3], _],
            [_, [1, 1, 3], _, _, _, [7], _, _, _, _],
            [_, _, _, _, [2, 3], _, _, _, [2, 3], _],
            [_, [3, 3], _, _, _, _, _, _, [2, 4], _],
            [_, [2, 3], _, _, _, [1, 1, 3], _, _, _, [1, 1, 1]],
            [_, _, _, _, _, _, _, _, [2, 4], _],
            [_, _, _, _, _, [1, 3], _, _, _, _],
        ])
        expected_solution = Grid([
            [X, X, X, _, _, _, X, X, X, X],
            [X, _, X, X, X, X, X, _, _, X],
            [_, X, X, _, _, X, _, _, _, X],
            [X, _, X, _, X, X, X, _, _, X],
            [X, _, _, X, X, _, X, _, _, X],
            [X, _, X, X, _, X, X, X, _, X],
            [X, _, X, _, _, X, _, X, _, X],
            [X, _, X, X, X, _, X, X, X, _],
            [X, _, _, X, _, X, X, _, _, X],
            [X, X, X, X, X, _, X, X, X, X]
        ])

        game_solver = TapaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_grid_10x10_evil(self):
        """https://gridpuzzle.com/tapa/jmn01"""
        grid = Grid([
            [_, _, [2], _, _, [4], _, _, _, _],
            [[2], _, _, _, _, _, _, _, [1, 3], _],
            [_, _, _, _, _, _, [5], [2], [1, 2], _],
            [[2], _, [2, 2], _, _, _, _, _, _, _],
            [_, _, _, _, _, _, [1, 2], _, [4], _],
            [_, [5], _, [6], _, _, _, _, _, _],
            [_, _, _, _, _, _, _, [3, 3], _, [4]],
            [_, [5], [2], [1, 1], _, _, _, _, _, _],
            [_, [5], _, _, _, _, _, _, _, [4]],
            [_, _, _, _, [1, 2], _, _, [4], _, _],
        ])
        expected_solution = Grid([
            [_, _, _, _, X, _, _, X, X, _],
            [_, _, X, X, X, X, X, X, _, _],
            [X, X, X, _, _, X, _, _, _, X],
            [_, _, _, _, X, X, _, _, _, X],
            [_, _, X, X, X, _, _, _, _, X],
            [_, _, X, _, X, X, X, _, X, X],
            [X, X, X, _, _, _, X, _, X, _],
            [X, _, _, _, _, _, X, _, X, _],
            [X, _, _, _, X, X, X, X, X, _],
            [X, X, X, X, _, _, _, _, X, X]
        ])

        game_solver = TapaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_grid_15x15_1(self):
        grid = Grid([
            [_, _, _, [1, 2], _, _, _, _, _, _, _, [1, 2], [2], [1, 1], _],
            [_, [7], _, _, [6], _, _, _, _, [7], _, _, _, _, _],
            [_, [1, 2, 2], _, _, _, _, _, [6], _, _, _, _, _, [1, 3], _],
            [[1, 2], _, _, _, _, _, _, _, _, _, [1, 4], _, _, [1, 3], _],
            [_, _, _, [1, 1, 3], _, _, _, [1, 5], _, _, _, [1, 3], _, _, _],
            [_, _, _, _, [1, 4], _, [1, 4], _, _, _, _, _, _, _, _],
            [_, [7], _, _, _, _, _, _, [2, 4], _, _, [6], _, _, [1, 2]],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [[2, 2], _, _, [7], _, _, [5], _, _, _, _, _, _, [3, 3], _],
            [_, _, _, _, _, _, _, _, [2, 3], _, [4], _, _, _, _],
            [_, _, _, [1, 5], _, _, _, [1, 3], _, _, _, [1, 2], _, _, _],
            [_, [2, 3], _, _, [1, 5], _, _, _, _, _, _, _, _, _, [1, 3]],
            [_, [7], _, _, _, _, _, [2, 3], _, _, _, _, _, [1, 2, 2], _],
            [_, _, _, _, _, [2, 3], _, _, _, _, [6], _, _, [7], _],
            [_, [3], [3], [1, 2], _, _, _, _, _, _, _, [1, 2], _, _, _]
        ])
        expected_solution = Grid([
            [X, X, X, _, X, X, _, _, X, X, X, _, _, _, _],
            [X, _, X, _, _, X, X, X, X, _, _, X, X, _, X],
            [X, _, X, X, X, X, _, _, X, X, X, X, _, _, X],
            [_, X, _, X, _, X, _, X, X, _, _, X, _, _, X],
            [_, X, X, _, X, X, X, _, X, X, _, _, X, _, X],
            [X, _, X, X, _, X, _, X, X, _, _, X, X, X, X],
            [X, _, X, _, _, X, _, _, _, X, _, _, X, _, _],
            [X, X, X, X, X, X, X, X, X, X, X, X, X, _, X],
            [_, _, X, _, X, _, _, X, _, X, _, _, X, _, X],
            [X, X, X, X, _, _, _, X, _, X, _, _, X, _, X],
            [_, _, X, _, X, X, _, _, _, X, X, _, X, X, X],
            [X, _, X, X, _, X, X, X, X, X, _, _, _, X, _],
            [X, _, X, _, X, X, _, _, _, X, X, X, X, _, X],
            [X, X, X, X, _, _, _, X, X, X, _, _, X, _, X],
            [_, _, _, _, X, X, X, X, _, X, X, _, X, X, X]
        ])

        game_solver = TapaSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
