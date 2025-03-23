import unittest
from unittest import TestCase

from Domain.Grid.Grid import Grid
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine
from Tapa.TapaSolver import TapaSolver


class TapaSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_not_grid(self):
        grid = Grid([[1],])
        with self.assertRaises(ValueError) as context:
            TapaSolver(grid, self.get_solver_engine())

        self.assertEqual("The grid must be at least 2x2", str(context.exception))

    def test_solution_grid_without_list_numbers(self):
        grid = Grid([
            [1, 1],
            [False, 1]
        ])
        with self.assertRaises(ValueError) as context:
            TapaSolver(grid, self.get_solver_engine())

        self.assertEqual("The grid must contain at least one list number", str(context.exception))

    def test_solution_grid_with_too_small_number(self):
        grid = Grid([
            [[-1], [1]],
            [False, [1]]
        ])
        with self.assertRaises(ValueError) as context:
            game_solver = TapaSolver(grid, self.get_solver_engine())

            game_solver.get_solution()
        self.assertEqual("Number must be positive and less than 9", str(context.exception))

    def test_solution_grid_with_too_big_number(self):
        grid = Grid([
            [[9], [1]],
            [False, [1]]
        ])
        with self.assertRaises(ValueError) as context:
            game_solver = TapaSolver(grid, self.get_solver_engine())

            game_solver.get_solution()
        self.assertEqual("Number must be positive and less than 9", str(context.exception))

    def test_solution_not_exist_white_on_number(self):
        grid = Grid([
            [[1], [1]],
            [[1], [1]],
        ])
        game_solver = TapaSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_not_exist_black_count_around_1_number(self):
        grid = Grid([
            [[4], False],
            [False, False],
        ])
        game_solver = TapaSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_exist_basic_grid_1_number(self):
        grid = Grid([
            [[3], False],
            [False, False],
        ])
        expected_solution = Grid([[False, True], [True, True]])
        game_solver = TapaSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_exist_basic_grid_number_0(self):
        grid = Grid([
            [False, False, False, False],
            [False, [0], False, False],
            [False, False, False, [0]],
            [False, False, [1], False],
        ])
        expected_solution = Grid([[False, False, False, False], [False, False, False, False], [False, False, False, False], [True, True, False, False]])
        game_solver = TapaSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_exist_basic_grid_1_number_8(self):
        grid = Grid([
            [False, False, False],
            [False, [8], False],
            [False, False, False],
        ])
        expected_solution = Grid([[True, True, True], [True, False, True], [True, True, True]])
        game_solver = TapaSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_exist_basic_grid_2_numbers(self):
        grid = Grid([
            [[2], False],
            [[2], False],
        ])
        expected_solution = Grid([[False, True], [False, True]])
        game_solver = TapaSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_not_exist_black_square(self):
        grid = Grid([
            [[1], [2], [2], [1]],
            [[2], False, False, [2]],
            [[2], False, False, [2]],
            [[1], [2], [2], [1]],

        ])
        game_solver = TapaSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_not_exist_black_count_around_2_numbers(self):
        grid = Grid([
            [[3, 1], False],
            [False, False],
        ])
        game_solver = TapaSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_not_exist_black_count_around_2_numbers_without_gap(self):
        grid = Grid([
            [[2, 1], False],
            [False, False],
        ])
        game_solver = TapaSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_exist_grid_with_list_count_1_1(self):
        grid = Grid([
            [[1, 1], False, False],
            [False, [7], False],
            [False, False, False],
        ])
        expected_solution = Grid([[False, True, True], [True, False, True], [True, True, True]])
        game_solver = TapaSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_exist_grid_with_list_count_2_2(self):
        grid = Grid([
            [False, False, False, False],
            [False, [7], [2, 2], False],
            [False, False, False, False],
            [[2], False, False, [1]],
        ])
        expected_solution = Grid([
            [True, True, True, False],
            [True, False, False, False],
            [True, True, True, False],
            [False, False, False, False]
        ])
        game_solver = TapaSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_not_exist_isolated_black(self):
        grid = Grid([
            [[2], False],
            [False, [2]],
        ])
        game_solver = TapaSolver(grid, self.get_solver_engine())

        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_grid_6x6(self):
        grid = Grid([
            [[1, 1], False, False, False, False, [1]],
            [False, False, False, False, False, False],
            [False, False, False, False, False, False],
            [False, [7], False, False, [5], False],
            [False, False, [1, 1, 2], [1, 4], False, False],
            [[2], False, False, False, False, [3]],
        ])
        expected_solution = Grid([
            [False, True, True, False, False, False],
            [True, False, True, True, True, False],
            [True, True, True, False, True, True],
            [True, False, True, False, False, True],
            [True, True, False, False, True, True],
            [False, False, True, True, True, False]
        ])
        game_solver = TapaSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_grid_10x10(self):
        grid = Grid([
            [[2], False, False, False, False, False, False, False, False, [2]],
            [False, False, False, [6], [1, 3], [1, 3], [2, 2], False, False, False],
            [False, False, False, False, False, False, False, False, False, False],
            [False, [3], False, [6], False, False, [2, 3], False, [7], False],
            [False, False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False, False],
            [False, False, False, False, [6], [1, 4], False, False, False, False],
            [False, [3], False, False, False, False, False, False, [3, 3], False],
            [False, [4], False, False, [6], [1, 3], False, False, [2, 4], False],
            [False, False, [1, 2], False, False, False, False, [1, 1, 1], False, False]
        ])
        expected_solution = Grid([
            [False, False, True, True, False, False, True, True, True, False],
            [True, True, True, False, False, False, False, False, True, False],
            [False, False, True, True, True, True, True, False, True, True],
            [False, False, True, False, True, False, False, True, False, True],
            [False, False, True, False, False, False, True, True, True, True],
            [True, True, True, True, True, True, True, False, False, True],
            [True, False, False, True, False, False, True, True, False, True],
            [True, False, False, True, True, False, False, True, False, True],
            [True, False, False, True, False, False, False, True, False, True],
            [True, True, False, True, True, True, True, False, True, True]
        ])
        game_solver = TapaSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_grid_10x10_2(self):
        grid = Grid([
            [False, False, False, False, [3], False, False, False, False, False],
            [False, [7], False, False, False, False, False, False, False, False],
            [[1, 1, 1], False, False, False, [6], False, False, False, [3], False],
            [False, [2, 3], False, False, False, False, False, False, [3], False],
            [False, [1, 1, 3], False, False, False, [7], False, False, False, False],
            [False, False, False, False, [2, 3], False, False, False, [2, 3], False],
            [False, [3, 3], False, False, False, False, False, False, [2, 4], False],
            [False, [2, 3], False, False, False, [1, 1, 3], False, False, False, [1, 1, 1]],
            [False, False, False, False, False, False, False, False, [2, 4], False],
            [False, False, False, False, False, [1, 3], False, False, False, False],
        ])
        expected_solution = Grid([
            [True, True, True, False, False, False, True, True, True, True],
            [True, False, True, True, True, True, True, False, False, True],
            [False, True, True, False, False, True, False, False, False, True],
            [True, False, True, False, True, True, True, False, False, True],
            [True, False, False, True, True, False, True, False, False, True],
            [True, False, True, True, False, True, True, True, False, True],
            [True, False, True, False, False, True, False, True, False, True],
            [True, False, True, True, True, False, True, True, True, False],
            [True, False, False, True, False, True, True, False, False, True],
            [True, True, True, True, True, False, True, True, True, True]
        ])
        game_solver = TapaSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solution_grid_15x15_1(self):
        grid = Grid([
            [False, False, False, [1, 2], False, False, False, False, False, False, False, [1, 2], [2], [1, 1], False],
            [False, [7], False, False, [6], False, False, False, False, [7], False, False, False, False, False],
            [False, [1, 2, 2], False, False, False, False, False, [6], False, False, False, False, False, [1, 3], False],
            [[1, 2], False, False, False, False, False, False, False, False, False, [1, 4], False, False, [1, 3], False],
            [False, False, False, [1, 1, 3], False, False, False, [1, 5], False, False, False, [1, 3], False, False, False],
            [False, False, False, False, [1, 4], False, [1, 4], False, False, False, False, False, False, False, False],
            [False, [7], False, False, False, False, False, False, [2, 4], False, False, [6], False, False, [1, 2]],
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            [[2, 2], False, False, [7], False, False, [5], False, False, False, False, False, False, [3, 3], False],
            [False, False, False, False, False, False, False, False, [2, 3], False, [4], False, False, False, False],
            [False, False, False, [1, 5], False, False, False, [1, 3], False, False, False, [1, 2], False, False, False],
            [False, [2, 3], False, False, [1, 5], False, False, False, False, False, False, False, False, False, [1, 3]],
            [False, [7], False, False, False, False, False, [2, 3], False, False, False, False, False, [1, 2, 2], False],
            [False, False, False, False, False, [2, 3], False, False, False, False, [6], False, False, [7], False],
            [False, [3], [3], [1, 2], False, False, False, False, False, False, False, [1, 2], False, False, False]
        ])
        expected_solution = Grid([
            [True, True, True, False, True, True, False, False, True, True, True, False, False, False, False],
            [True, False, True, False, False, True, True, True, True, False, False, True, True, False, True],
            [True, False, True, True, True, True, False, False, True, True, True, True, False, False, True],
            [False, True, False, True, False, True, False, True, True, False, False, True, False, False, True],
            [False, True, True, False, True, True, True, False, True, True, False, False, True, False, True],
            [True, False, True, True, False, True, False, True, True, False, False, True, True, True, True],
            [True, False, True, False, False, True, False, False, False, True, False, False, True, False, False],
            [True, True, True, True, True, True, True, True, True, True, True, True, True, False, True],
            [False, False, True, False, True, False, False, True, False, True, False, False, True, False, True],
            [True, True, True, True, False, False, False, True, False, True, False, False, True, False, True],
            [False, False, True, False, True, True, False, False, False, True, True, False, True, True, True],
            [True, False, True, True, False, True, True, True, True, True, False, False, False, True, False],
            [True, False, True, False, True, True, False, False, False, True, True, True, True, False, True],
            [True, True, True, True, False, False, False, True, True, True, False, False, True, False, True],
            [False, False, False, False, True, True, True, True, False, True, True, False, True, True, True]
        ])
        game_solver = TapaSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)


if __name__ == '__main__':
    unittest.main()
