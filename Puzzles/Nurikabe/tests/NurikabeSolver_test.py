import unittest
from unittest import TestCase

from Puzzles.Nurikabe.NurikabeSolver import NurikabeSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine
from Utils.Grid import Grid


class NurikabeSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_grid_must_be_at_least_5x5_raises_value_error_column(self):
        grid = Grid([
            [1, 1, 1, 2],
            [1, 3, 1, 1],
            [1, 3, 3, 4],
            [1, 1, 3, 4],
            [1, 3, 3, 4],
        ])
        with self.assertRaises(ValueError) as context:
            NurikabeSolver(grid, NurikabeSolverTests.get_solver_engine())
        self.assertEqual(str(context.exception), "The grid must be at least 5x5")

    def test_grid_must_be_at_least_5x5_raises_value_error_row(self):
        grid = Grid([
            [1, 1, 1, 2, 2],
            [1, 3, 1, 1, 1],
            [1, 3, 3, 4, 4],
            [1, 1, 3, 4, 4],
        ])
        with self.assertRaises(ValueError) as context:
            NurikabeSolver(grid, NurikabeSolverTests.get_solver_engine())
        self.assertEqual(str(context.exception), "The grid must be at least 5x5")

    def test_get_solution_5x5_only_numbers_1(self):
        grid = Grid([
            [1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [1, 0, 1, 0, 0],
            [0, 0, 0, 0, 1],
        ])
        expected_solution = Grid([
            [0, 1, 0, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 0, 1, 0, 1],
            [0, 1, 0, 1, 1],
            [1, 1, 1, 1, 0]
        ])
        game_solver = NurikabeSolver(grid, NurikabeSolverTests.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_5x5_only_numbers_1_when_not_possible(self):
        grid = Grid([
            [0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0],
            [1, 0, 0, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 1, 0, 0, 0],
        ])
        game_solver = NurikabeSolver(grid, NurikabeSolverTests.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_get_solution_5x5_numbers_1_2(self):
        grid = Grid([
            [0, 0, 1, 0, 0],
            [0, 2, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0],
        ])
        expected_solution = Grid([
            [1, 1, 0, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 1, 1, 1],
            [1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1]
        ])
        game_solver = NurikabeSolver(grid, NurikabeSolverTests.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_5x5_numbers_1_2_bis(self):
        grid = Grid([
            [0, 2, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 2, 0, 0],
            [0, 0, 0, 0, 0],
            [2, 0, 0, 0, 2],
        ])
        expected_solution = Grid([
            [1, 0, 1, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 1, 0, 1, 1],
            [0, 1, 0, 1, 0],
            [0, 1, 1, 1, 0]
        ])
        game_solver = NurikabeSolver(grid, NurikabeSolverTests.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_5x5_only_numbers_2(self):
        grid = Grid([
            [0, 0, 0, 2, 0],
            [2, 0, 0, 0, 0],
            [0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0],
            [0, 2, 0, 2, 0],
        ])
        expected_solution = Grid([
            [1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0],
            [1, 0, 1, 1, 1],
            [1, 0, 1, 0, 0],
        ])
        game_solver = NurikabeSolver(grid, NurikabeSolverTests.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_5x5_with_island_size_6(self):
        grid = Grid([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 6, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [1, 1, 1, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
        ])
        game_solver = NurikabeSolver(grid, NurikabeSolverTests.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_5x5_1(self):
        grid = Grid([
            [2, 0, 0, 4, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
        ])
        expected_solution = Grid([
            [0, 0, 1, 0, 1],
            [1, 1, 1, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1],
        ])
        game_solver = NurikabeSolver(grid, NurikabeSolverTests.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_5x5_2(self):
        grid = Grid([
            [0, 0, 0, 0, 1],
            [0, 0, 2, 0, 0],
            [0, 0, 0, 2, 0],
            [2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [1, 1, 1, 1, 0],
            [1, 0, 0, 1, 1],
            [1, 1, 1, 0, 1],
            [0, 0, 1, 0, 1],
            [1, 1, 1, 1, 1],
        ])
        game_solver = NurikabeSolver(grid, NurikabeSolverTests.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_5x5_3(self):
        grid = Grid([
            [0, 5, 0, 0, 3],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 2, 0],
            [0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [0, 0, 1, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 0, 0, 1],
            [1, 1, 1, 1, 1],
        ])
        game_solver = NurikabeSolver(grid, NurikabeSolverTests.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_5x5_4(self):  # approx 28 ms
        grid = Grid([
            [1, 0, 0, 3, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [1, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [0, 1, 1, 0, 0],
            [1, 1, 0, 1, 0],
            [1, 0, 1, 1, 1],
            [1, 1, 0, 0, 1],
            [0, 1, 1, 1, 1],
        ])
        game_solver = NurikabeSolver(grid, NurikabeSolverTests.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_5x5_5(self):  # approx 40 ms
        grid = Grid([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0],
            [0, 1, 0, 0, 3],
            [1, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1],
            [1, 0, 1, 1, 0],
            [0, 1, 1, 0, 0],
        ])
        game_solver = NurikabeSolver(grid, NurikabeSolverTests.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_5x5_6(self):  # approx 34 ms
        grid = Grid([
            [1, 0, 0, 0, 0],
            [0, 0, 1, 0, 2],
            [0, 0, 0, 0, 0],
            [0, 0, 3, 0, 1],
            [0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [0, 1, 1, 1, 0],
            [1, 1, 0, 1, 0],
            [1, 0, 1, 1, 1],
            [1, 0, 0, 1, 0],
            [1, 1, 1, 1, 1]
        ])
        game_solver = NurikabeSolver(grid, NurikabeSolverTests.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_7x7_easy(self):  # approx 300 ms
        grid = Grid([
            [0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [5, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0, 4],
        ])
        expected_solution = Grid([
            [1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 0],
            [1, 1, 1, 1, 1, 1, 0],
            [1, 0, 0, 1, 0, 1, 1],
            [1, 1, 0, 1, 0, 0, 0],
        ])
        game_solver = NurikabeSolver(grid, NurikabeSolverTests.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_get_solution_12x(self):  # approx 4,8 seconds
        grid = Grid([
            [0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 2, 0, 3, 0, 1, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 7, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
        ])
        expected_solution = Grid([
            [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
            [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
        ])
        game_solver = NurikabeSolver(grid, NurikabeSolverTests.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip("This test takes too long to run")  # TODO:
    def test_get_solution_10x10(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 6, 0, 0, 5, 0],
            [5, 0, 0, 0, 0, 0, 0, 3, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 2, 0, 0, 0, 0, 0, 0, 5],
            [0, 2, 0, 0, 5, 0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
            [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
        ])
        game_solver = NurikabeSolver(grid, NurikabeSolverTests.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
