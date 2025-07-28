import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Chocona.ChoconaSolver import ChoconaSolver

_ = -1


class ChoconaSolverTests(TestCase):
    def test_basic_numbers_constraints(self):
        numbers_grid = Grid([
            [3, _, 0],
            [_, 1, _],
            [0, _, 1],
        ])
        regions_grid = Grid([
            [1, 1, 2],
            [1, 3, 2],
            [4, 4, 5]
        ])

        expected_grid = Grid([
            [1, 1, 0],
            [1, 1, 0],
            [0, 0, 1]
        ])
        game_solver = ChoconaSolver(numbers_grid, regions_grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_basic_numbers_and_square_constraints(self):
        numbers_grid = Grid([
            [3, _, 0],
            [_, _, _],
            [_, _, 1],
        ])
        regions_grid = Grid([
            [1, 1, 2],
            [1, 3, 2],
            [4, 4, 5]
        ])

        expected_grid = Grid([
            [1, 1, 0],
            [1, 1, 0],
            [0, 0, 1]
        ])
        game_solver = ChoconaSolver(numbers_grid, regions_grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_easy_31yz6_square(self):
        """https://gridpuzzle.com/chocona/31yz6"""
        numbers_grid = Grid([
            [4, _, _, 1],
            [_, _, _, _],
            [1, 1, 3, _],
            [_, _, _, _],
        ])
        regions_grid = Grid([
            [1, 1, 1, 2],
            [1, 1, 1, 2],
            [3, 4, 5, 5],
            [3, 4, 4, 5]
        ])

        expected_grid = Grid([
            [1, 1, 0, 1],
            [1, 1, 0, 0],
            [0, 0, 1, 1],
            [1, 0, 1, 1]
        ])
        game_solver = ChoconaSolver(numbers_grid, regions_grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_evil_1n50r(self):
        """https://gridpuzzle.com/chocona/1n50r"""
        numbers_grid = Grid([
            [3, _, _, _],
            [0, _, 4, _],
            [2, _, _, _],
            [_, _, _, _],
        ])
        regions_grid = Grid([
            [1, 1, 1, 1],
            [2, 2, 3, 3],
            [4, 2, 2, 3],
            [4, 3, 3, 3]
        ])

        expected_grid = Grid([
            [1, 0, 1, 1],
            [0, 0, 1, 1],
            [1, 0, 0, 0],
            [1, 0, 1, 1]
        ])
        game_solver = ChoconaSolver(numbers_grid, regions_grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x7_expert_0pd11(self):
        """https://gridpuzzle.com/chocona/0pd11"""
        numbers_grid = Grid([
            [4, _, 4, _, _, _, 4],
            [_, _, _, _, _, _, _],
            [0, 4, _, _, _, _, _],
            [_, _, _, _, 1, _, _],
            [_, 6, _, _, _, 0, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, 3, _, _],
        ])
        regions_grid = Grid([
            [1, 1, 2, 2, 2, 2, 3],
            [1, 1, 1, 2, 2, 3, 3],
            [4, 5, 5, 2, 2, 3, 3],
            [5, 5, 5, 5, 6, 6, 6],
            [5, 7, 5, 5, 5, 8, 6],
            [5, 7, 7, 7, 8, 8, 6],
            [7, 7, 7, 7, 9, 9, 9],
        ])

        expected_grid = Grid([
            [1, 1, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 1, 0, 1],
            [1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 0, 1, 1, 1]
        ])
        game_solver = ChoconaSolver(numbers_grid, regions_grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_9x9_evil_0mmg2(self):
        """https://gridpuzzle.com/chocona/0mmg2"""
        numbers_grid = Grid([
            [_, 2, 2, 1, _, _, 2, _, _],
            [_, _, _, 3, _, 2, _, _, 1],
            [7, _, _, _, 2, _, _, _, _],
            [_, _, _, _, 2, _, _, _, _],
            [_, _, _, _, _, 8, 4, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [5, _, _, _, _, 1, 0, _, 2],
            [_, _, _, _, _, _, _, _, _],
        ])
        regions_grid = Grid([
            [1, 2, 3, 4, 4, 4, 5, 5, 5],
            [2, 2, 3, 6, 4, 7, 7, 7, 8],
            [9, 2, 6, 6, 10, 10, 7, 8, 8],
            [9, 6, 6, 6, 11, 11, 11, 8, 8],
            [9, 9, 9, 6, 6, 12, 13, 13, 13],
            [9, 9, 9, 12, 12, 12, 12, 13, 13],
            [9, 9, 9, 12, 12, 12, 12, 12, 12],
            [14, 14, 14, 12, 12, 15, 16, 16, 17],
            [14, 14, 14, 14, 12, 15, 15, 15, 17],
        ])

        expected_grid = Grid([
            [0, 1, 1, 0, 1, 0, 1, 1, 0],
            [0, 1, 1, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 1],
            [1, 1, 0, 1, 1, 1, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 1, 1, 0, 0, 1, 1],
            [1, 1, 0, 1, 1, 0, 1, 0, 0],
            [1, 1, 0, 1, 1, 0, 0, 0, 1],
            [1, 1, 0, 1, 1, 0, 1, 0, 1]
        ])
        game_solver = ChoconaSolver(numbers_grid, regions_grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_9x9_evil_1jped(self):
        """https://gridpuzzle.com/chocona/1jped"""
        numbers_grid = Grid([
            [1, 2, _, _, 2, _, _, 3, 2],
            [_, 3, 1, _, _, _, _, _, _],
            [_, _, _, _, _, 11, 1, _, _],
            [1, 0, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [2, _, _, _, 1, 0, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, 5, _, _, 8, _, _, _, _],
            [1, _, _, _, _, _, _, _, _]
        ])
        regions_grid = Grid([
            [1, 2, 2, 2, 3, 3, 4, 5, 6],
            [1, 7, 8, 8, 8, 8, 5, 5, 6],
            [7, 7, 8, 8, 9, 10, 11, 5, 6],
            [20, 12, 12, 10, 10, 10, 11, 5, 5],
            [20, 12, 12, 10, 10, 10, 10, 10, 10],
            [16, 12, 12, 12, 15, 14, 14, 10, 10],
            [16, 16, 15, 15, 15, 10, 10, 10, 10],
            [16, 17, 17, 17, 18, 18, 18, 18, 18],
            [19, 19, 17, 17, 18, 18, 18, 18, 18],
        ])

        expected_grid = Grid([
            [0, 0, 1, 1, 1, 1, 0, 0, 1],
            [1, 1, 0, 0, 0, 0, 1, 0, 1],
            [1, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 1, 1, 1],
            [0, 1, 1, 1, 0, 1, 1, 1, 1],
            [0, 1, 1, 1, 0, 1, 1, 1, 1]
        ])
        game_solver = ChoconaSolver(numbers_grid, regions_grid)

        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
