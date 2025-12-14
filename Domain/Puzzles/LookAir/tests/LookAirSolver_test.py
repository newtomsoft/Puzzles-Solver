import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.LookAir.LookAirSolver import LookAirSolver

_ = -1


class LookAirSolverTests(TestCase):
    def test_solution_numbers_contraints(self):
        grid = Grid([
            [3, _, 1],
            [_, 3, 1],
            [_, 1, _],
        ])

        game_solver = LookAirSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 0],
            [1, 1, 0],
            [0, 0, 0]
        ])
        self.assertEqual(expected_solution, solution)

    def test_solution_squares2x2_contraints(self):
        grid = Grid([
            [3, _, _],
            [_, _, 1],
            [_, 1, _],
        ])

        game_solver = LookAirSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 0],
            [1, 1, 0],
            [0, 0, 0]
        ])
        self.assertEqual(expected_solution, solution)

    def test_solution_squares3x3_contraints(self):
        grid = Grid([
            [_, _, _, _],
            [_, 5, _, 1],
            [_, _, _, _],
            [_, 1, _, 0],
        ])

        game_solver = LookAirSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 0],
            [1, 1, 1, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 0]
        ])
        self.assertEqual(expected_solution, solution)

    def test_solution_6x6_without_visibility_constraint(self):
        grid = Grid([
            [1, 2, _, _, 1, _],
            [2, _, _, 1, _, _],
            [0, 1, _, 1, 3, _],
            [_, _, 1, _, 1, 2],
            [_, _, 2, _, _, 1],
            [3, _, 2, _, 1, 1],
        ])

        game_solver = LookAirSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 1],
            [0, 0, 0, 0, 1, 1],
            [0, 0, 1, 0, 0, 0],
            [1, 1, 0, 0, 0, 1],
            [1, 1, 0, 1, 0, 0]
        ])
        self.assertEqual(expected_solution, solution)

    def test_solution_10x10_without_visibility_constraint(self):
        grid = Grid([
            [1, 3, 3, _, 1, 1, 1, _, _, _],
            [1, _, 3, _, _, _, _, 2, _, 2],
            [_, 1, _, 1, 1, _, 3, _, 3, 1],
            [_, 2, _, _, 1, _, _, 3, _, _],
            [1, _, 3, 3, 3, _, 1, _, 0, _],
            [_, _, _, 3, _, 1, 2, 1, _, 1],
            [_, _, 1, _, _, 1, _, _, 3, _],
            [0, 1, _, 4, _, _, 2, _, 3, _],
            [1, _, 4, _, _, _, _, 3, _, 2],
            [_, _, _, 4, 3, 2, _, 3, 2, 1]
        ])

        game_solver = LookAirSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [0, 1, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 1, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 1, 0, 0],
            [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1],
            [0, 0, 1, 1, 1, 0, 1, 1, 0, 0],
            [1, 0, 1, 1, 1, 0, 1, 1, 0, 1]
        ])
        self.assertEqual(expected_solution, solution)

    def test_solution_5x5_easy_316e9(self):
        """https://gridpuzzle.com/look-air/316e9"""
        grid = Grid([
            [3, _, _, _, 1],
            [_, 3, _, 1, _],
            [1, _, 1, _, 3],
            [2, _, 2, 3, _],
            [1, 2, _, _, 1],
        ])

        game_solver = LookAirSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 0, 0, 1],
            [1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1],
            [0, 1, 0, 1, 1],
            [1, 0, 0, 0, 0]
        ])
        self.assertEqual(expected_solution, solution)

    def test_solution_empty_5x5_not_compliant_visibility(self):
        grid = Grid([
            [3, 3, _, 3, 3],
            [3, 3, _, 3, 3],
            [_, _, _, _, _],
            [0, 0, 0, 0, 0],
            [_, _, _, _, _]
        ])

        game_solver = LookAirSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_empty_8x8_not_compliant_visibility(self):
        grid = Grid([
            [3, 3, _, _, 2, 1, 3, 3],
            [3, 3, 1, _, 1, _, 3, 3],
            [_, _, _, _, 1, _, _, _],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])

        game_solver = LookAirSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 0, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])
        self.assertEqual(expected_solution, solution)

    def test_solution_5x5_evil_0ywpw(self):
        """https://gridpuzzle.com/look-air/0ywpw"""
        grid = Grid([
            [_, _, _, 3, _],
            [2, _, 3, _, _],
            [_, 3, _, 1, _],
            [_, _, 2, _, 1],
            [_, 2, _, _, _],
        ])

        game_solver = LookAirSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 0, 1, 1, 0],
            [0, 0, 1, 1, 0],
            [1, 1, 0, 0, 0],
            [1, 1, 0, 0, 1],
            [0, 0, 1, 0, 0]
        ])
        self.assertEqual(expected_solution, solution)

    def test_solution_5x5_evil_16dp9(self):
        """https://gridpuzzle.com/look-air/16dp9"""
        grid = Grid([
            [_, _, 3, _, _],
            [1, _, _, _, _],
            [1, _, 1, _, 1],
            [_, _, _, _, _],
            [_, _, 2, _, 1]
        ])

        game_solver = LookAirSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 0, 1, 1, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 0, 0, 1],
            [1, 1, 0, 0, 0],
            [1, 1, 0, 1, 0]
        ])
        self.assertEqual(expected_solution, solution)

    def test_solution_6x6_evil_2pp6y(self):
        """https://gridpuzzle.com/look-air/2pp6y"""
        grid = Grid([
            [_, _, 3, _, 1, _],
            [_, _, _, 1, _, _],
            [_, _, 2, _, _, _],
            [_, _, _, _, _, 1],
            [_, _, _, 3, _, _],
            [_, 2, _, _, _, _],
        ])

        game_solver = LookAirSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [0, 1, 1, 0, 1, 0],
            [0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 1, 0]
        ])
        self.assertEqual(expected_solution, solution)

    def test_solution_6x6_easy_1y159(self):
        """https://gridpuzzle.com/look-air/1y159"""
        grid = Grid([
            [1, 2, _, _, _, 1],
            [2, _, _, 1, _, _],
            [0, 1, _, 1, _, _],
            [_, _, 1, _, 1, 2],
            [_, _, 2, _, _, 1],
            [3, _, _, _, 1, 1],
        ])

        game_solver = LookAirSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 1],
            [0, 0, 0, 0, 1, 1],
            [0, 0, 1, 0, 0, 0],
            [1, 1, 0, 0, 0, 1],
            [1, 1, 0, 1, 0, 0]
        ])
        self.assertEqual(expected_solution, solution)

    def test_solution_7x7_easy_09pk8(self):
        """https://gridpuzzle.com/look-air/09pk8"""
        grid = Grid([
            [1, _, 1, _, 3, _, 1],
            [_, _, _, 1, _, 3, 2],
            [2, _, _, _, 1, _, 1],
            [_, 3, 1, _, 2, 1, _],
            [3, _, 2, _, _, _, 0],
            [2, 2, _, 3, _, _, _],
            [1, _, 3, _, 1, _, 0]
        ])

        game_solver = LookAirSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [0, 0, 1, 0, 1, 1, 0],
            [1, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 0, 0, 1, 0],
            [1, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 1, 0, 0, 0],
            [1, 0, 1, 1, 0, 0, 0]
        ])
        self.assertEqual(expected_solution, solution)

    def test_solution_7x7_evil_0m912(self):
        """https://gridpuzzle.com/look-air/0m912"""
        grid = Grid([
            [_, 1, _, _, _, 2, _],
            [_, 0, _, _, _, _, _],
            [_, _, _, 1, _, 1, _],
            [_, _, 1, _, _, _, _],
            [1, _, _, _, _, _, _],
            [_, _, 1, _, _, 3, _],
            [_, _, _, _, 1, _, 1]
        ])

        game_solver = LookAirSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 0, 0, 1, 1, 0, 1],
            [0, 0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 1],
            [0, 0, 0, 1, 0, 1, 1],
            [0, 0, 0, 0, 1, 0, 0]
        ])
        self.assertEqual(expected_solution, solution)

    def test_solution_8x8_easy_6er9n(self):
        """https://gridpuzzle.com/look-air/6er9n"""
        grid = Grid([
            [1, _, 3, _, 1, 2, _, _],
            [_, 3, _, _, 2, _, 2, _],
            [1, _, 2, _, _, 2, 1, 1],
            [3, _, 3, _, 1, _, _, _],
            [_, 5, 4, _, 3, _, 2, 1],
            [3, _, 3, _, _, 3, _, _],
            [_, 2, 2, _, 2, 2, 3, 3],
            [1, 1, _, _, _, 1, _, 3]
        ])

        game_solver = LookAirSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [0, 1, 1, 0, 1, 0, 0, 0],
            [0, 1, 1, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0],
            [1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 1, 1, 0, 1],
            [1, 1, 1, 0, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 1],
            [0, 1, 0, 0, 0, 0, 1, 1]
        ])
        self.assertEqual(expected_solution, solution)

    def test_solution_10x10_evil_07141(self):
        """https://gridpuzzle.com/look-air/07141"""
        grid = Grid([
            [_, _, 3, _, _, _, 3, _, _, _],
            [_, _, _, 3, _, _, _, _, _, _],
            [1, 1, _, _, _, _, _, _, _, _],
            [_, _, _, 4, _, _, _, _, 2, _],
            [_, 2, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, 3, _],
            [_, 1, _, _, _, _, 1, _, _, _],
            [_, _, _, _, _, _, _, _, 2, 2],
            [_, _, _, _, _, _, 1, _, _, _],
            [_, _, _, 2, _, _, _, 1, _, _]
        ])

        game_solver = LookAirSolver(grid)

        solution = game_solver.get_solution()
        expected_solution = Grid([
            [0, 0, 1, 1, 0, 0, 1, 1, 1, 0],
            [0, 0, 1, 1, 0, 0, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 0, 0, 1, 1],
            [0, 0, 1, 1, 1, 1, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [0, 0, 1, 0, 1, 1, 0, 0, 1, 0]
        ])
        self.assertEqual(expected_solution, solution)

        
if __name__ == '__main__':
    unittest.main()
