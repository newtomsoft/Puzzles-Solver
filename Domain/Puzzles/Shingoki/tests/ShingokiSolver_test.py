import unittest
from unittest import TestCase

from Domain.Grid.Grid import Grid
from Shingoki.ShingokiSolver import ShingokiSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine


class ShingokiSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_black2_not_loop(self):
        grid = Grid([
            ['b2', ' '],
            [' ', ' ']
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_white_horizontal_w2(self):
        grid = Grid([
            [' ', 'w2', ' '],
            [' ', 'w2', ' '],
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_horizontal_w3(self):
        grid = Grid([
            [' ', ' ', 'w3', ' '],
            [' ', 'w3', ' ', ' '],
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌────────┐ \n'
            ' └────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_vertical_w2(self):
        grid = Grid([
            [' ', ' '],
            ['w2', 'w2'],
            [' ', ' '],
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐ \n'
            ' │  │ \n'
            ' └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_vertical_w3(self):
        grid = Grid([
            [' ', ' '],
            ['w3', ' '],
            [' ', 'w3'],
            [' ', ' '],
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐ \n'
            ' │  │ \n'
            ' │  │ \n'
            ' └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_horizontal_vertical_0(self):
        grid = Grid([
            [' ', 'w2', ' '],
            ['w2', ' ', ' '],
            [' ', 'w2', ' ']
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' │     │ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_horizontal_vertical_1(self):
        grid = Grid([
            [' ', 'w3', ' ', ' '],
            ['w3', ' ', ' ', 'w2'],
            [' ', ' ', ' ', ' '],
            [' ', 'w2', ' ', ' ']
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌────────┐ \n'
            ' │        │ \n'
            ' │     ┌──┘ \n'
            ' └─────┘    '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_horizontal_vertical_2(self):
        grid = Grid([
            [' ', 'w3', ' ', ' '],
            ['w3', ' ', ' ', ' '],
            [' ', ' ', 'w2', ' '],
            [' ', 'w2', ' ', ' ']
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌────────┐ \n'
            ' │     ┌──┘ \n'
            ' │     │    \n'
            ' └─────┘    '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_right_down_b2_4(self):
        grid = Grid([
            [' ', 'b2', ' '],
            ['b2', ' ', ' '],
            [' ', ' ', 'b4'],
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            '    ┌──┐ \n'
            ' ┌──┘  │ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_right_down_b3(self):
        grid = Grid([
            [' ', 'b3', ' ', ' '],
            ['b3', ' ', ' ', ' '],
            [' ', 'b3', ' ', ' '],
            [' ', ' ', ' ', ' '],
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            '    ┌─────┐ \n'
            ' ┌──┘     │ \n'
            ' │  ┌─────┘ \n'
            ' └──┘       '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_right_up_b2_4(self):
        grid = Grid([
            [' ', ' ', 'b4'],
            ['b2', ' ', ' '],
            [' ', 'b2', ' '],
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' └──┐  │ \n'
            '    └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_right_up_b3(self):
        grid = Grid([
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            ['b3', ' ', 'b3', ' '],
            [' ', 'b3', ' ', ' '],
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐    \n'
            ' │     │    \n'
            ' └──┐  └──┐ \n'
            '    └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_left_down_b2_4(self):
        grid = Grid([
            [' ', 'b2', ' '],
            [' ', ' ', 'b2'],
            ['b4', ' ', ' '],
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐    \n'
            ' │  └──┐ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_left_down_b3(self):
        grid = Grid([
            [' ', ' ', 'b3', ' '],
            [' ', 'b3', ' ', 'b3'],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐    \n'
            ' └──┐  └──┐ \n'
            '    │     │ \n'
            '    └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_left_up_b2_4(self):
        grid = Grid([
            ['b4', ' ', ' '],
            [' ', ' ', 'b2'],
            [' ', 'b2', ' '],
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' │  ┌──┘ \n'
            ' └──┘    '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_black(self):
        grid = Grid([
            [' ', 'w2', ' '],
            [' ', ' ', 'b2'],
            [' ', ' ', ' '],
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' │  ┌──┘ \n'
            ' └──┘    '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_0(self):
        grid = Grid([
            [' ', ' ', ' ', ' ', ' ', ' '],
            ['b5', ' ', 'w2', ' ', ' ', ' '],
            [' ', ' ', ' ', 'w4', ' ', 'b2'],
            [' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', 'b6', ' ', 'b2'],
            [' ', 'w4', ' ', ' ', ' ', ' '],
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            '    ┌──┐  ┌──┐    \n'
            ' ┌──┘  │  │  └──┐ \n'
            ' │  ┌──┘  │  ┌──┘ \n'
            ' │  │     │  └──┐ \n'
            ' │  └─────┘  ┌──┘ \n'
            ' └───────────┘    '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_1(self):
        grid = Grid([
            ['b6', ' ', ' ', 'w5', ' ', ' '],
            [' ', ' ', 'b6', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'b4'],
            [' ', 'b2', ' ', ' ', ' ', ' '],
            [' ', 'w2', ' ', 'b5', ' ', ' '],
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──────────────┐ \n'
            ' └──┐  ┌─────┐  │ \n'
            ' ┌──┘  │  ┌──┘  │ \n'
            ' └──┐  │  │  ┌──┘ \n'
            ' ┌──┘  │  │  └──┐ \n'
            ' └─────┘  └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_2(self):
        grid = Grid([
            [' ', ' ', ' ', 'w3', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'b2'],
            [' ', ' ', ' ', 'b3', 'b2', ' '],
            ['b4', ' ', ' ', ' ', ' ', ' '],
            [' ', 'b2', ' ', ' ', ' ', ' '],
            [' ', 'w2', ' ', 'b4', ' ', 'b3'],
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  ┌────────┐ \n'
            ' │  │  └──┐  ┌──┘ \n'
            ' │  └─────┘  └──┐ \n'
            ' └──┐  ┌──┐  ┌──┘ \n'
            ' ┌──┘  │  │  └──┐ \n'
            ' └─────┘  └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_0(self):
        grid = Grid([
            [' ', ' ', ' ', ' ', ' ', 'w6', ' ', ' '],
            [' ', 'w3', ' ', ' ', ' ', 'b6', 'b4', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'b4', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' '],
            [' ', 'b2', ' ', ' ', ' ', ' ', 'b3', ' '],
            ['b4', 'b2', ' ', ' ', ' ', 'b3', ' ', ' '],
            [' ', ' ', 'b3', ' ', ' ', 'b3', ' ', ' ']
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            '    ┌─────────────────┐ \n'
            '    │  ┌────────┐  ┌──┘ \n'
            '    │  │        │  │    \n'
            ' ┌──┘  └─────┐  │  │    \n'
            ' │  ┌─────┐  │  └──┘    \n'
            ' │  └──┐  │  └─────┐    \n'
            ' └──┐  │  └─────┐  └──┐ \n'
            '    └──┘        └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_1(self):
        grid = Grid([
            [' ', ' ', ' ', ' ', ' ', 'b5', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'b4', ' ', ' ', ' ', ' ', ' ', 'w3'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'b4', ' ', 'w4', 'w6', 'b4', ' ', ' '],
            ['w6', 'b2', ' ', ' ', ' ', ' ', ' ', 'w3'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b4']
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            '    ┌───────────┐  ┌──┐ \n'
            ' ┌──┘  ┌─────┐  └──┘  │ \n'
            ' │  ┌──┘     │  ┌──┐  │ \n'
            ' │  │  ┌──┐  │  │  └──┘ \n'
            ' │  │  │  │  │  │  ┌──┐ \n'
            ' │  └──┘  │  │  └──┘  │ \n'
            ' │  ┌──┐  │  │  ┌──┐  │ \n'
            ' └──┘  └──┘  └──┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_11x11(self):
        grid = Grid([
            ['b3', ' ', ' ', 'b2', ' ', ' ', 'b2', ' ', ' ', 'w2', ' '],
            [' ', ' ', ' ', 'b3', ' ', ' ', 'b3', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' '],
            [' ', 'b2', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' '],
            ['b6', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', 'w2', ' ', ' '],
            [' ', ' ', ' ', ' ', 'b2', 'b2', ' ', ' ', ' ', 'b4', ' '],
            [' ', 'w2', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', 'w5'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', 'b2', ' ', ' '],
            [' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', 'b2', ' ', ' '],
            [' ', 'b2', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', 'b2'],
            [' ', ' ', ' ', 'w4', ' ', 'b5', ' ', ' ', ' ', 'b5', ' ']
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐     ┌──┐     ┌──┐  ┌─────┐ \n'
            ' │  └─────┘  └─────┘  │  │  ┌──┘ \n'
            ' └──┐  ┌──┐  ┌─────┐  │  │  └──┐ \n'
            '    └──┘  │  └──┐  │  │  └──┐  │ \n'
            ' ┌─────┐  └─────┘  │  └─────┘  │ \n'
            ' │  ┌──┘     ┌──┐  └────────┐  │ \n'
            ' │  │     ┌──┘  └──┐     ┌──┘  │ \n'
            ' │  └──┐  └─────┐  │  ┌──┘  ┌──┘ \n'
            ' └──┐  │  ┌─────┘  │  └──┐  └──┐ \n'
            ' ┌──┘  └──┘  ┌──┐  └─────┘  ┌──┘ \n'
            ' └───────────┘  └───────────┘    '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_16x16(self):
        grid = Grid([
            [' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', 'b3', 'b4', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', 'w2', ' ', 'w2', 'w2', ' ', ' ', ' ', 'w3'],
            [' ', ' ', 'w3', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', 'w3', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'b5', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'w4', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', 'b3', ' ', 'w3', ' ', ' '],
            [' ', ' ', ' ', 'w3', 'w5', 'w4', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', 'b4', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', 'w2', ' '],
            ['w15', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' '],
            [' ', 'w11', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', 'b3', 'b2', ' ', ' ', ' ', ' ', 'b6'],
            [' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' '],
            [' ', ' ', ' ', ' ', 'b2', 'b5', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', 'b2', ' ', ' '],
            [' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' ', ' ', 'b2', 'b3'],
            [' ', 'w2', ' ', ' ', ' ', 'b2', ' ', ' ', 'b2', 'b3', ' ', ' ', ' ', 'b3', ' ', 'b2'],
            [' ', ' ', 'b2', ' ', 'b3', ' ', 'b2', ' ', ' ', ' ', ' ', 'b3', 'w2', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'w6', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  ┌──┐  ┌──┐     ┌──┐  ┌──┐  ┌─────┐  ┌──┐ \n'
            ' │  │  │  └──┘  └──┐  │  │  │  │  │  ┌──┘  │  │ \n'
            ' │  │  │  ┌──┐  ┌──┘  │  └──┘  └──┘  │  ┌──┘  │ \n'
            ' │  │  └──┘  │  └─────┘  ┌────────┐  └──┘  ┌──┘ \n'
            ' │  │  ┌──┐  │  ┌──┐  ┌──┘  ┌─────┘  ┌─────┘    \n'
            ' │  │  │  │  │  │  │  │     └─────┐  └────────┐ \n'
            ' │  │  │  │  │  │  │  │  ┌────────┘  ┌─────┐  │ \n'
            ' │  │  │  └──┘  │  └──┘  └──┐  ┌─────┘     │  │ \n'
            ' │  │  └──┐  ┌──┘  ┌─────┐  │  └──┐     ┌──┘  │ \n'
            ' │  │  ┌──┘  └──┐  └──┐  │  └──┐  └──┐  └─────┘ \n'
            ' │  │  └─────┐  └─────┘  └──┐  └──┐  └──┐  ┌──┐ \n'
            ' │  └──┐  ┌──┘  ┌───────────┘     └──┐  └──┘  │ \n'
            ' │  ┌──┘  └──┐  └──┐  ┌───────────┐  └──┐  ┌──┘ \n'
            ' │  │  ┌──┐  │  ┌──┘  └──┐  ┌──┐  └─────┘  └──┐ \n'
            ' │  └──┘  └──┘  └──┐  ┌──┘  │  │  ┌─────┐  ┌──┘ \n'
            ' └─────────────────┘  └─────┘  └──┘     └──┘    '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip('This test is too slow (around 10 seconds)')
    def test_solution_21x21(self):
        grid = Grid([
            [' ', ' ', ' ', ' ', 'b5', 'w2', ' ', ' ', ' ', ' ', 'w6', ' ', ' ', ' ', 'b7', ' ', 'w5', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', 'b4', 'b4', ' '],
            ['w4', ' ', 'b3', 'w7', ' ', 'b5', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'b2', 'b4', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', 'w3', 'b2', ' ', ' ', 'b2', ' ', ' '],
            ['b4', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', 'b3', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'b5', 'b2', 'w4', ' ', ' ', ' ', ' ', ' ', 'b5', ' ', 'b3', ' ', ' ', ' ', ' '],
            [' ', ' ', 'b2', ' ', ' ', 'b6', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', 'b2', 'b2', ' ', ' ', ' ', 'b3', ' ', ' '],
            [' ', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', 'b6', ' ', 'b2', ' ', ' ', ' ', 'b3', ' ', ' ', ' '],
            [' ', ' ', 'b3', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', 'b2', 'b2', ' ', 'b2'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', 'w2', 'w2', ' '],
            [' ', ' ', ' ', 'b2', ' ', 'w3', ' ', ' ', ' ', ' ', 'w2', 'b4', ' ', 'b6', 'w4', 'w3', ' ', ' ', ' ', 'b3', ' '],
            [' ', ' ', 'b3', 'w2', 'b6', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', 'b5', ' ', ' ', ' '],
            [' ', 'w5', 'b4', ' ', ' ', ' ', 'w3', 'b4', ' ', 'b4', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', 'w2', ' ', 'b4', ' ', 'w4', ' ', 'b4', ' ', 'b4', 'w2', ' ', ' '],
            [' ', 'b6', ' ', 'b3', ' ', ' ', ' ', 'b3', 'w4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w5', 'b2', ' ', ' ', 'b2'],
            [' ', ' ', ' ', ' ', ' ', 'w2', 'b5', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' ', 'w3', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' '],
            [' ', ' ', ' ', 'b4', 'b2', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', 'b5']
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  ┌──┐  ┌─────┐     ┌─────────────────┐  ┌──────────────┐ \n'
            ' │  │  │  │  │  ┌──┘     └──┐  ┌──┐  ┌──┐  └──┘  ┌─────┐  ┌──┘ \n'
            ' │  └──┘  │  │  └───────────┘  │  └──┘  └─────┐  │     │  │    \n'
            ' │  ┌──┐  │  └──┐  ┌───────────┘  ┌─────┐  ┌──┘  │  ┌──┘  │    \n'
            ' └──┘  │  │     │  │     ┌─────┐  │  ┌──┘  │  ┌──┘  └──┐  └──┐ \n'
            ' ┌──┐  │  │     │  └──┐  │  ┌──┘  │  │     │  └──┐     └─────┘ \n'
            ' │  └──┘  │     │  ┌──┘  │  │     │  │     └─────┘  ┌──┐       \n'
            ' │  ┌──┐  └─────┘  │     │  └──┐  │  └──┐  ┌──┐     │  └─────┐ \n'
            ' └──┘  └────────┐  │  ┌──┘  ┌──┘  └──┐  └──┘  └──┐  └──┐  ┌──┘ \n'
            '    ┌──┐     ┌──┘  │  │  ┌──┘  ┌─────┘  ┌─────┐  │  ┌──┘  └──┐ \n'
            ' ┌──┘  │     │  ┌──┘  │  └─────┘  ┌─────┘  ┌──┘  │  └──┐  ┌──┘ \n'
            ' └──┐  └──┐  │  │     └────────┐  │        │  ┌──┘     │  │    \n'
            '    │  ┌──┘  │  │              │  └─────┐  │  │  ┌─────┘  └──┐ \n'
            '    │  └─────┘  └─────┐  ┌─────┘  ┌──┐  │  │  │  │  ┌────────┘ \n'
            '    │  ┌──┐  ┌────────┘  │  ┌─────┘  │  │  └──┘  │  │          \n'
            '    │  │  └──┘  ┌──┐     │  │     ┌──┘  │  ┌──┐  │  └─────┐    \n'
            ' ┌──┘  │  ┌─────┘  └──┐  │  └──┐  │  ┌──┘  │  │  │  ┌──┐  └──┐ \n'
            ' └──┐  └──┘  ┌─────┐  │  └──┐  │  │  └──┐  │  │  └──┘  │  ┌──┘ \n'
            '    └──┐     └──┐  │  └─────┘  │  └──┐  │  │  └─────┐  │  │    \n'
            ' ┌─────┘  ┌──┐  │  │  ┌──┐  ┌──┘     │  └──┘  ┌──┐  └──┘  └──┐ \n'
            ' └────────┘  └──┘  └──┘  └──┘        └────────┘  └───────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip('This test is too slow (around 21 seconds)')
    def test_solution_26x26(self):
        grid = Grid([
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w11', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', 'b2', ' ', ' '],
            [' ', 'b2', 'b3', ' ', 'b2', ' ', ' ', ' ', 'b5', 'w3', ' ', ' ', ' ', 'w5', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', 'w2', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', 'b6', ' ', 'b5', 'b2', ' ', ' ', ' ', ' ', ' ', 'w2', 'b3', 'b5', ' ', 'b3', 'b4', ' ', ' ', ' ', ' ', 'w2', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'w6', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'b4', ' ', 'w5', ' ', ' ', 'w2', ' ', 'b2', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', 'w2', ' ', ' ', 'b5'],
            ['b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', 'b4'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', 'b6', 'w5', 'b3', ' ', ' ', 'b2', ' ', ' '],
            ['w4', ' ', ' ', 'w6', ' ', 'w2', ' ', 'w2', ' ', 'w4', 'b2', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', 'b3', 'w3', ' ', 'b2', ' '],
            [' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', 'b8', 'w5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' '],
            ['w4', 'b2', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', 'w6', ' ', ' ', 'w3', ' ', 'b5', ' ', ' ', ' ', 'b3', ' ', ' '],
            [' ', 'b3', 'b2', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b8', 'b3', 'b2'],
            [' ', ' ', ' ', 'w2', ' ', ' ', ' ', 'w2', ' ', ' ', 'b3', 'b3', ' ', ' ', ' ', ' ', 'w3', ' ', 'w2', ' ', 'b3', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', 'w2', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' ', ' '],
            ['b3', ' ', ' ', 'b2', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' '],
            ['b2', 'b4', ' ', ' ', ' ', 'b8', ' ', ' ', 'w5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w7', 'b4', 'b2'],
            [' ', ' ', 'b7', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b7', ' ', ' ', 'w5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'w7', ' ', 'w4', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', 'b3', 'b3', ' ', ' ', ' ', ' ', 'b2', 'b2', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w4', 'b3', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', 'b4', ' ', 'b4', 'b5', ' ', 'w3', ' ', ' ', 'b4', ' ', ' ', ' ', 'b2', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'b6', 'b5', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w5', ' ', ' ', 'b2', ' ', ' ', ' ', 'b2'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b8', ' ', ' ', ' ', ' '],
            [' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', 'w6', 'b5', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', 'w4', ' ', ' ', ' ', 'b5', 'b3', 'b5'],
            [' ', ' ', 'b3', ' ', ' ', 'b3', ' ', ' ', 'w2', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', 'b4', 'w2', ' ', ' ', 'b4', ' ', 'w3', ' ', ' '],
            ['b5', ' ', ' ', 'w4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', 'w2', 'b2', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', 'b2', ' ', ' '],
            [' ', ' ', ' ', ' ', 'w5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', 'w2', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', ' '],
            [' ', 'w3', ' ', ' ', ' ', ' ', ' ', ' ', 'w6', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b10']
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            '    ┌─────┐  ┌──┐  ┌────────────────────────────────┐  ┌────────┐  ┌──┐  ┌──┐ \n'
            '    └──┐  └──┘  │  └──┐  ┌────────┐  ┌──────────────┘  └──┐  ┌──┘  │  └──┘  │ \n'
            ' ┌──┐  │  ┌──┐  │  ┌──┘  │     ┌──┘  └─────┐  ┌─────┐  ┌──┘  └──┐  └─────┐  │ \n'
            ' │  └──┘  │  │  │  │  ┌──┘     └─────┐  ┌──┘  │  ┌──┘  │  ┌──┐  │     ┌──┘  │ \n'
            ' │  ┌──┐  │  │  │  │  │     ┌──┐     │  └──┐  │  │     │  │  │  └─────┘  ┌──┘ \n'
            ' └──┘  │  │  │  │  │  └─────┘  └──┐  └──┐  └──┘  └─────┘  │  └────────┐  └──┐ \n'
            ' ┌──┐  │  │  │  └──┘  ┌──┐  ┌──┐  └──┐  └──────────────┐  │  ┌─────┐  └──┐  │ \n'
            ' │  └──┘  │  └─────┐  │  │  │  └──┐  └────────┐  ┌─────┘  │  └──┐  │  ┌──┘  │ \n'
            ' │  ┌─────┘        └──┘  │  │     │  ┌─────┐  │  └────────┘     │  │  │  ┌──┘ \n'
            ' │  └──┐  ┌─────┐  ┌─────┘  │  ┌──┘  └──┐  │  │  ┌────────┐  ┌──┘  └──┘  │    \n'
            ' └──┐  └──┘  ┌──┘  └──┐  ┌──┘  └─────┐  │  │  │  │  ┌──┐  │  └──┐  ┌──┐  └──┐ \n'
            '    │  ┌─────┘        │  │  ┌──┐  ┌──┘  │  │  │  │  │  │  └──┐  │  │  │  ┌──┘ \n'
            '    └──┘           ┌──┘  │  │  │  │  ┌──┘  │  └──┘  │  └──┐  │  │  │  │  │    \n'
            ' ┌─────┐  ┌──┐     └──┐  │  │  └──┘  │     │  ┌─────┘     └──┘  │  │  │  │    \n'
            ' └──┐  └──┘  └──┐  ┌──┘  │  └──┐  ┌──┘     └──┘                 └──┘  │  └──┐ \n'
            '    │  ┌─────┐  │  │  ┌──┘     │  │     ┌──────────────┐  ┌──┐        │  ┌──┘ \n'
            '    │  │  ┌──┘  │  │  │  ┌──┐  │  └──┐  │  ┌──┐  ┌─────┘  │  │  ┌──┐  │  └──┐ \n'
            ' ┌──┘  │  └──┐  │  │  │  │  │  └──┐  └──┘  │  │  └─────┐  │  └──┘  └──┘  ┌──┘ \n'
            ' └──┐  │     │  │  │  │  │  └─────┘  ┌─────┘  └────────┘  │  ┌────────┐  └──┐ \n'
            ' ┌──┘  │  ┌──┘  │  └──┘  └──┐  ┌──┐  │     ┌──────────────┘  └──┐     │  ┌──┘ \n'
            ' │  ┌──┘  └──┐  │     ┌─────┘  │  └──┘     └────────────────────┘     │  │    \n'
            ' │  └─────┐  │  └──┐  │  ┌──┐  │  ┌──┐           ┌───────────┐  ┌─────┘  └──┐ \n'
            ' │  ┌──┐  │  │  ┌──┘  │  │  │  │  │  │     ┌──┐  │  ┌─────┐  │  └────────┐  │ \n'
            ' └──┘  │  │  │  │     └──┘  │  │  │  │     │  └──┘  │  ┌──┘  │     ┌──┐  │  │ \n'
            ' ┌─────┘  │  │  └───────────┘  │  │  └─────┘  ┌─────┘  └──┐  └─────┘  └──┘  │ \n'
            ' └────────┘  └─────────────────┘  └───────────┘           └─────────────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip('This test is too slow (around 92 seconds)')
    def test_solution_31x31(self):
        grid = Grid([
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', 'w3', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', 'b3', 'b4', ' ', ' ', 'b2', ' ', ' ', ' ', ' '],
            [' ', 'b2', ' ', 'b2', ' ', 'w2', 'b3', ' ', ' ', ' ', ' ', ' ', 'b3', 'w2', ' ', 'w2', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', 'b4'],
            [' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', ' '],
            [' ', 'w2', ' ', ' ', ' ', 'w3', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['b5', ' ', ' ', 'b2', ' ', ' ', ' ', 'b5', ' ', ' ', 'b2', 'w2', ' ', 'w4', ' ', ' ', ' ', ' ', ' ', 'b3', 'b3', 'b2', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', 'b4', ' '],
            [' ', ' ', ' ', 'b4', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', ' '],
            [' ', ' ', 'w3', ' ', ' ', ' ', 'b4', 'w4', 'w2', ' ', ' ', 'w3', ' ', ' ', 'b3', ' ', ' ', 'b6', ' ', ' ', ' ', 'w2', ' ', 'w3', 'b5', ' ', ' ', 'b5', ' ', ' ', ' '],
            [' ', ' ', 'w3', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', 'b4', 'b3', ' ', ' ', ' ', 'b4', ' ', 'w4', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'b2', 'b3', 'w2', ' ', ' ', ' ', ' ', 'b4', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'b3', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', 'b4', 'w2', ' ', 'w2', ' ', 'w3', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', 'b4'],
            [' ', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', 'w4', ' ', 'w2', ' ', ' '],
            [' ', 'b5', 'w2', ' ', ' ', 'b3', ' ', 'w3', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', 'b2'],
            [' ', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', 'w2', ' ', ' ', 'b2', 'b3', ' ', ' ', ' ', ' ', 'b3', 'w2', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', 'w2', ' ', ' ', 'w3', ' '],
            [' ', ' ', 'w2', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', 'b3'],
            [' ', ' ', ' ', ' ', ' ', 'b2', 'b6', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', 'b2', 'b2', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b5', ' '],
            ['b3', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', 'b2', ' ', 'w2', ' ', 'b3', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', 'w4', ' ', ' ', ' ', 'w3', ' ', ' '],
            [' ', ' ', 'b2', ' ', 'b10', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', 'w2', ' ', ' ', ' ', 'b3', ' ', ' ', 'b6', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b10'],
            [' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', 'b2', ' ', 'b2', 'b3', ' ', ' ', ' ', 'b4', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' '],
            [' ', 'b3', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', 'b2', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'w8', 'b5', ' ', 'w4', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', 'b2', ' ', ' ', ' ', 'w9'],
            ['w7', ' ', 'b2', ' ', ' ', ' ', 'b6', ' ', ' ', ' ', ' ', 'b7', ' ', ' ', ' ', ' ', 'w2', 'w3', ' ', 'b3', ' ', 'b3', 'w3', 'b4', ' ', ' ', ' ', 'b3', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w6', ' ', 'b4', ' ', ' ', ' ', 'b6', ' ', ' ', ' ', 'b4', ' ', 'b4', 'b2', 'b4', ' ', ' ', 'b6', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', 'w6', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', 'b4', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', 'w5', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' '],
            [' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w6', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', 'b5', ' ', ' ', 'b4', ' ', ' ', ' ', ' '],
            ['w7', 'b8', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w6', ' ', 'b2', ' ', 'b2', ' ', 'b2', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', 'w4', ' ', 'b6', ' ', ' ', 'b4', ' ', 'b7', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'b6', 'w3', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', 'b4', ' ', 'b2', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'b6', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', 'w2', ' ', 'w3', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', 'b3', 'w4', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', 'b3', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b16', ' ', ' ', ' ', ' ', ' ', 'w7', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  ┌──┐     ┌──┐     ┌──┐  ┌────────┐     ┌──┐  ┌─────┐  ┌─────┐  ┌──┐     ┌──┐          \n'
            ' │  └──┘  └──┐  │  └─────┘  └──┘  ┌──┐  │     │  │  │  ┌──┘  │  ┌──┘  │  └─────┘  └────────┐ \n'
            ' │  ┌─────┐  └──┘  ┌────────┐  ┌──┘  │  └─────┘  └──┘  └──┐  │  └──┐  │  ┌─────┐  ┌────────┘ \n'
            ' │  │     └────────┘        │  └──┐  └───────────┐  ┌──┐  │  └──┐  │  └──┘     │  │          \n'
            ' └──┘     ┌──┐     ┌──┐     └──┐  │  ┌───────────┘  │  └──┘  ┌──┘  │  ┌──┐     │  └─────┐    \n'
            ' ┌────────┘  │     │  │  ┌──┐  └──┘  │  ┌────────┐  │        │  ┌──┘  │  │     └─────┐  │    \n'
            ' └────────┐  └─────┘  │  │  └────────┘  └──┐  ┌──┘  └────────┘  │     │  └────────┐  │  └──┐ \n'
            ' ┌────────┘     ┌──┐  │  └────────┐  ┌──┐  │  └──┐  ┌───────────┘     └────────┐  │  └──┐  │ \n'
            ' └──┐  ┌─────┐  │  │  └──┐  ┌─────┘  │  │  └──┐  │  │        ┌───────────┐     │  └─────┘  │ \n'
            '    └──┘     └──┘  └──┐  │  │  ┌─────┘  └──┐  │  │  └─────┐  │  ┌────────┘     └─────┐  ┌──┘ \n'
            '          ┌────────┐  │  │  └──┘     ┌──┐  └──┘  └─────┐  └──┘  │     ┌───────────┐  │  │    \n'
            '    ┌─────┘  ┌──┐  │  │  └─────┐  ┌──┘  └─────┐  ┌─────┘     ┌──┘     │  ┌─────┐  └──┘  └──┐ \n'
            '    │  ┌─────┘  │  │  └─────┐  └──┘  ┌─────┐  └──┘  ┌─────┐  │     ┌──┘  └──┐  │  ┌────────┘ \n'
            '    │  │     ┌──┘  │     ┌──┘  ┌─────┘  ┌──┘  ┌─────┘  ┌──┘  └─────┘  ┌──┐  │  └──┘     ┌──┐ \n'
            '    └──┘     └──┐  └─────┘  ┌──┘        └──┐  └──┐     └───────────┐  │  │  └───────────┘  │ \n'
            ' ┌──┐           └──┐  ┌──┐  └─────┐  ┌─────┘  ┌──┘  ┌──┐  ┌────────┘  │  │  ┌──┐  ┌────────┘ \n'
            ' │  └──┐  ┌──┐     │  │  └──┐  ┌──┘  └─────┐  └─────┘  │  │  ┌────────┘  │  │  │  │     ┌──┐ \n'
            ' └──┐  └──┘  │  ┌──┘  └──┐  └──┘  ┌─────┐  │  ┌────────┘  │  │  ┌────────┘  │  └──┘  ┌──┘  │ \n'
            '    └─────┐  │  │  ┌─────┘        └──┐  └──┘  └─────┐  ┌──┘  │  └──┐  ┌─────┘  ┌──┐  └──┐  │ \n'
            ' ┌──┐     │  │  │  └───────────┐     └───────────┐  │  │  ┌──┘     │  │     ┌──┘  │     │  │ \n'
            ' │  │  ┌──┘  │  │  ┌────────┐  └──┐  ┌────────┐  │  │  │  └─────┐  │  └─────┘  ┌──┘     │  │ \n'
            ' │  │  └──┐  │  │  │        └──┐  │  │  ┌──┐  │  └──┘  └────────┘  └──┐  ┌──┐  └────────┘  │ \n'
            ' │  │     │  │  │  │  ┌──┐     │  │  │  │  │  │  ┌─────────────────┐  │  │  └──┐  ┌─────┐  │ \n'
            ' │  │  ┌──┘  │  │  └──┘  └──┐  │  │  │  │  │  └──┘  ┌──────────────┘  │  │     └──┘     │  │ \n'
            ' │  │  └──┐  │  │  ┌─────┐  │  │  │  │  │  └──┐     └──┐  ┌──┐  ┌─────┘  └─────┐  ┌─────┘  │ \n'
            ' │  └─────┘  └──┘  │  ┌──┘  │  │  │  │  │  ┌──┘  ┌──┐  └──┘  │  └───────────┐  │  └──┐  ┌──┘ \n'
            ' └──┐  ┌───────────┘  │  ┌──┘  │  └──┘  │  └─────┘  └─────┐  │  ┌────────┐  └──┘  ┌──┘  │    \n'
            ' ┌──┘  └───────────┐  │  │     └────────┘        ┌────────┘  │  └─────┐  │  ┌──┐  └──┐  │    \n'
            ' └──────────────┐  │  └──┘     ┌──┐     ┌──┐     │  ┌────────┘  ┌─────┘  │  │  └─────┘  │    \n'
            ' ┌──────────────┘  └───────────┘  └─────┘  │  ┌──┘  └───────────┘  ┌─────┘  │  ┌─────┐  └──┐ \n'
            ' └─────────────────────────────────────────┘  └────────────────────┘        └──┘     └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip('This test is too slow (around 69 seconds)')
    def test_solution_36x36(self):
        grid = Grid([
            [' ', ' ', 'w5', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w8', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' '],
            ['b2', ' ', ' ', ' ', 'b6', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', 'b4', 'b3', ' ', ' ', 'b2', ' ', 'w2', ' ', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', 'b2'],
            [' ', ' ', ' ', ' ', ' ', 'w3', ' ', 'b2', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w7', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', ' ', 'w7', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', ' '],
            [' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', 'b4', ' ', ' ', ' ', 'b4', ' ', 'b3', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' '],
            ['b3', ' ', ' ', ' ', ' ', ' ', 'b6', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', 'b5', ' ', ' ', ' ', 'b6', ' ', ' ', ' ', ' ', ' ', 'b7', ' ', ' ', ' ', ' ', 'w6', ' ', ' ', ' ', ' ', ' '],
            ['w2', ' ', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', 'b3', ' ', ' ', ' ', ' ', 'b7', ' ', 'w3', ' ', ' ', ' ', 'w4', 'b9', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', 'b3', ' ', ' ', ' ', 'w6', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', ' '],
            [' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', 'w4', ' ', ' ', ' ', ' ', ' ', 'b8', ' ', ' ', ' ', 'w3', ' ', 'b9', ' ', 'b8', 'w7', ' ', ' ', 'b2'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w6', ' ', ' ', ' ', 'w2', 'b5', ' ', 'b3', ' ', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'w2', 'w2', ' ', ' ', 'b6', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', 'w3', 'b4', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2'],
            [' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', 'w4', ' ', ' ', ' ', 'b2', ' ', 'b3', ' ', 'b3', ' ', ' ', ' ', 'b2', ' '],
            [' ', ' ', ' ', ' ', 'w5', ' ', ' ', ' ', 'b3', 'b2', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'w6', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', 'b2', ' ', ' ', ' ', ' ', 'b2', 'w2', 'w3', ' ', 'b2', ' ', 'b3', ' ', 'b3', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', 'b14', 'w2', ' '],
            [' ', ' ', ' ', 'b4', ' ', 'w5', ' ', 'b3', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b5', ' ', ' ', 'w3', ' ', ' ', ' ', 'w2', ' ', ' ', ' '],
            [' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', 'b2', ' ', 'w2', ' ', 'b5', 'b2', ' ', ' ', ' ', 'b4', ' ', 'b7', ' ', ' ', ' ', ' ', ' ', 'b9', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b7', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', 'b2', 'b3', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', 'b4', ' ', 'w2', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', 'w4', ' ', ' '],
            ['b9', ' ', 'b3', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', 'w3', ' ', 'w3', ' ', 'w3', ' ', ' ', ' '],
            [' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w13', ' '],
            [' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', 'w5', 'b3', ' ', ' ', ' ', ' ', 'b6', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w6', ' ', ' ', 'b6', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b6', ' ', ' ', 'w2', ' ', ' ', ' ', 'b5', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', 'b6', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'w5', ' ', ' ', 'w3', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w4', 'w2', 'b3', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b7', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b9', ' ', ' ', 'w4', ' ', ' ', 'w3', ' ', ' ', ' ', 'b3', ' ', 'b4', ' ', 'w4', ' ', ' ', 'b6', ' ', ' ', 'b3', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', 'b3', 'w3', ' ', ' ', ' ', 'b3', ' ', ' ', 'w5', 'b5', 'b3', ' ', ' ', ' ', ' ', ' ', 'b5', 'w4', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', 'w3', ' ', ' ', ' ', ' ', 'w7', ' ', ' '],
            [' ', 'w4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', 'b5', ' ', ' ', ' ', ' '],
            [' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' ', 'w4', ' ', 'w3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'w8', 'w5', ' ', ' ', ' ', 'w5', ' ', ' ', ' ', ' ', ' ', 'b6', 'w3', 'w3', 'b3', 'b2', ' ', 'b3', ' ', ' ', 'w3', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'b2', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', 'b2', 'b3', ' ', ' ', ' ', ' ', 'w8', ' ', ' ', 'b17'],
            ['w4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', ' ', 'b7', 'b5', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', 'b3', 'w2', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', 'b2', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', 'b2', ' ', 'w4', ' ', 'b2', ' ', 'b2'],
            [' ', ' ', 'w2', ' ', ' ', ' ', 'w2', ' ', 'w2', 'w2', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', 'w2', ' ', ' ', 'w3', ' ', ' ', ' ', 'b2', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'b3', ' ', 'w3', ' ', ' ', 'w3', ' ', ' ', 'w3', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', 'b4', ' ', 'b3', 'b2', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w9', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', 'b2', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', 'b2', 'b3']
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            '    ┌──────────────┐  ┌─────┐  ┌───────────────────────┐  ┌──┐     ┌──────────────┐        ┌──┐  ┌─────┐    \n'
            ' ┌──┘  ┌─────┐  ┌──┘  └──┐  │  └─────┐  ┌──┐  ┌─────┐  └──┘  │  ┌──┘  ┌────────┐  │  ┌─────┘  │  └──┐  └──┐ \n'
            ' └──┐  │     │  │     ┌──┘  └────────┘  │  │  └──┐  └──┐  ┌──┘  │  ┌──┘        │  │  │  ┌──┐  │     │  ┌──┘ \n'
            ' ┌──┘  └──┐  │  │     └────────┐  ┌─────┘  │  ┌──┘     │  └──┐  │  └────────┐  │  │  │  │  │  └──┐  │  └──┐ \n'
            ' └─────┐  │  │  └────────┐  ┌──┘  └──┐  ┌──┘  │        └─────┘  └──┐  ┌─────┘  │  │  │  │  │  ┌──┘  │  ┌──┘ \n'
            ' ┌──┐  │  │  └──┐  ┌──┐  │  │  ┌─────┘  └──┐  └────────┐  ┌────────┘  └─────┐  │  │  │  │  │  │     │  │    \n'
            ' │  └──┘  └──┐  │  │  │  │  │  │  ┌──┐     └────────┐  │  │  ┌───────────┐  │  │  │  │  │  │  │     │  │    \n'
            ' └─────┐  ┌──┘  │  │  │  │  │  └──┘  │     ┌──┐     │  │  │  │           │  │  │  └──┘  │  │  └──┐  │  └──┐ \n'
            ' ┌─────┘  │     │  │  │  │  └──┐     └─────┘  │     │  └──┘  │  ┌─────┐  │  │  └────────┘  └──┐  │  │  ┌──┘ \n'
            ' └──┐  ┌──┘     │  │  │  │     │  ┌─────┐  ┌──┘     │  ┌─────┘  └──┐  │  │  │        ┌──┐     │  │  │  │    \n'
            '    │  │        └──┘  │  └─────┘  └──┐  │  │  ┌─────┘  └──┐        │  │  │  └──┐  ┌──┘  └──┐  │  │  │  └──┐ \n'
            ' ┌──┘  └─────┐  ┌─────┘  ┌───────────┘  │  │  │  ┌─────┐  └─────┐  │  │  └──┐  └──┘  ┌─────┘  │  │  │  ┌──┘ \n'
            ' │  ┌─────┐  │  │  ┌─────┘  ┌──┐  ┌──┐  └──┘  └──┘  ┌──┘  ┌──┐  │  │  │     │  ┌─────┘        │  │  │  └──┐ \n'
            ' │  │     │  │  │  └────────┘  │  │  └─────┐  ┌──┐  │  ┌──┘  │  └──┘  │     │  └─────┐  ┌──┐  │  │  │  ┌──┘ \n'
            ' │  │     │  │  │  ┌─────┐  ┌──┘  └──┐  ┌──┘  │  │  │  └──┐  └──┐  ┌──┘     │  ┌─────┘  │  │  │  └──┘  │    \n'
            ' │  │  ┌──┘  │  │  └──┐  │  └─────┐  │  └─────┘  │  │  ┌──┘  ┌──┘  │     ┌──┘  └────────┘  │  └─────┐  └──┐ \n'
            ' │  │  └─────┘  └──┐  │  └─────┐  │  └──┐  ┌─────┘  └──┘     └─────┘     └─────────────────┘        └──┐  │ \n'
            ' │  │              │  └─────┐  │  │  ┌──┘  └──┐     ┌──┐  ┌─────────────────┐  ┌──┐     ┌──┐     ┌──┐  │  │ \n'
            ' │  └───────────┐  └─────┐  │  └──┘  └──┐  ┌──┘     │  └──┘  ┌──┐  ┌─────┐  └──┘  └─────┘  │     │  │  │  │ \n'
            ' └──┐  ┌─────┐  │  ┌──┐  │  │  ┌──┐     │  │        │  ┌─────┘  │  │     └──┐  ┌────────┐  │     │  │  │  │ \n'
            '    │  └──┐  │  │  │  │  │  └──┘  └─────┘  │     ┌──┘  └──┐     │  │        └──┘        │  └─────┘  │  │  │ \n'
            '    │  ┌──┘  │  └──┘  │  │  ┌──┐  ┌────────┘  ┌──┘  ┌─────┘  ┌──┘  └─────────────────┐  └───────────┘  │  │ \n'
            '    │  │     └────────┘  │  │  │  └──┐  ┌──┐  └──┐  └──┐     └──┐  ┌──────────────┐  │  ┌──┐     ┌──┐  │  │ \n'
            '    │  └────────┐  ┌──┐  └──┘  └──┐  └──┘  │  ┌──┘  ┌──┘  ┌──┐  └──┘              │  │  │  └─────┘  │  │  │ \n'
            ' ┌──┘     ┌──┐  │  │  │           └─────┐  │  └──┐  │     │  │  ┌────────┐  ┌─────┘  │  └────────┐  │  │  │ \n'
            ' │  ┌──┐  │  │  │  │  └───────────┐     │  │     │  │     │  │  └─────┐  │  │  ┌─────┘     ┌──┐  │  │  │  │ \n'
            ' └──┘  └──┘  │  │  └──┐  ┌─────┐  │  ┌──┘  └──┐  │  └─────┘  │        │  │  │  │  ┌────────┘  │  │  │  │  │ \n'
            ' ┌───────────┘  │  ┌──┘  └──┐  │  │  │  ┌──┐  │  │  ┌──┐  ┌──┘     ┌──┘  │  │  └──┘  ┌────────┘  │  │  │  │ \n'
            ' │  ┌────────┐  │  │  ┌──┐  │  │  │  │  │  │  │  │  │  │  │     ┌──┘  ┌──┘  └────────┘           │  │  │  │ \n'
            ' └──┘        │  │  │  │  │  │  │  │  │  │  │  └──┘  │  │  └──┐  │  ┌──┘  ┌────────┐     ┌──┐     │  └──┘  │ \n'
            ' ┌──┐  ┌─────┘  │  │  │  │  │  │  └──┘  │  │  ┌─────┘  └──┐  └──┘  │  ┌──┘  ┌──┐  └─────┘  └──┐  │  ┌─────┘ \n'
            ' │  └──┘  ┌─────┘  │  │  └──┘  └────────┘  └──┘           └────────┘  └─────┘  └───────────┐  │  │  └─────┐ \n'
            ' │  ┌─────┘  ┌─────┘  │  ┌──┐     ┌─────┐  ┌──┐  ┌──┐     ┌──┐        ┌──┐     ┌──┐  ┌──┐  │  │  └──┐  ┌──┘ \n'
            ' │  └─────┐  │  ┌─────┘  │  │     └──┐  └──┘  └──┘  └─────┘  └────────┘  └──┐  │  └──┘  └──┘  │  ┌──┘  └──┐ \n'
            ' └─────┐  │  │  └────────┘  └────────┘  ┌───────────┐  ┌─────┐  ┌────────┐  └──┘  ┌──┐  ┌─────┘  │  ┌──┐  │ \n'
            '       └──┘  └──────────────────────────┘           └──┘     └──┘        └────────┘  └──┘        └──┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        # other_solution = game_solver.get_other_solution()
        # self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip('This test is too slow (around 120 seconds)')
    def test_solution_41x41(self):
        grid = Grid([
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' ', 'b2', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', 'b2', ' ', ' ', 'b4', ' ', ' '],
            ['b8', ' ', 'b3', ' ', ' ', 'b2', 'b2', ' ', ' ', 'w2', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['w7', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', 'w2', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', 'b2', ' ', ' ', ' ', 'b4', ' ', 'w2', ' ', ' ', ' ', 'w3', ' '],
            [' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', 'w4', ' ', ' ', 'w5', 'w4', ' ', ' ', ' ', ' ', 'w4', 'w2', ' ', ' ', 'b3', ' ', ' ', 'b2', ' ', ' ', ' ', 'w4', ' ', ' ', ' ', ' ', 'b5', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'b3', 'w3', ' ', ' ', 'w2', ' ', ' ', ' ', 'b6', ' ', ' ', ' ', ' ', 'w5', 'w3', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', 'b8', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2'],
            [' ', ' ', 'w3', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', 'w3', 'w3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', 'w5', 'w2', ' ', ' ', ' ', ' ', 'b3', ' ', 'w2', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', ' '],
            [' ', 'w5', 'b4', ' ', 'w4', ' ', ' ', 'b6', ' ', ' ', 'b2', ' ', ' ', ' ', 'b6', 'b3', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' '],
            [' ', ' ', ' ', 'w4', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', 'b4', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', 'w2', ' ', ' ', 'b4', ' ', ' ', ' '],
            [' ', 'w3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', 'b3', 'w5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', 'b2', ' ', ' ', ' ', 'b8', ' ', 'w2', ' ', ' ', ' ', 'b3'],
            [' ', ' ', 'w5', ' ', 'b2', 'b6', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b7', ' ', ' ', ' ', ' ', 'b5', ' ', 'w3', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'w5', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', 'b4', ' ', 'b4'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b7', ' ', 'b5', 'b3', 'w2', 'b2', ' ', ' ', ' ', ' ', 'w5', 'b6', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', 'b6', ' ', ' ', ' ', 'b3', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'w6', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', 'w2', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', ' '],
            [' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', 'b2', ' ', 'b3', ' ', ' ', ' ', ' ', 'b2', ' ', 'w3', ' ', ' ', 'b2', 'w4', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'b2', ' ', ' ', 'w4', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'b5', ' ', 'b5', ' ', ' ', ' ', ' ', 'w2', 'b3', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', 'b2', ' ', ' ', ' ', ' ', 'b3', 'w2', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w4', 'w4', ' '],
            [' ', ' ', ' ', ' ', 'w3', ' ', 'b3', ' ', ' ', ' ', 'b4', 'w4', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', 'w2', ' ', 'w4', ' ', ' ', ' ', ' ', 'b3', 'w4', ' ', ' ', 'b5'],
            [' ', ' ', 'b7', ' ', ' ', 'b2', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', 'w3', ' ', ' ', ' ', 'b2', ' ', 'b3', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', 'b3', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', 'b7', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', 'b4', 'w6', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'w5', ' ', ' ', 'b2', 'b3', ' ', 'w3', 'b3', ' ', ' ', ' ', ' ', 'w6', 'w2', ' ', ' ', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', 'b2', ' ', ' ', 'b4', ' ', 'b7', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b5', ' ', ' ', 'b2', ' ', 'b7', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', 'w2', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', 'b3', 'w2', ' ', 'b3', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'b2', ' ', 'b2', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', 'b2', ' ', 'w3', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' '],
            ['b3', ' ', ' ', 'b5', ' ', ' ', ' ', 'b5', 'w2', ' ', ' ', ' ', 'b3', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b6', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'b2', ' ', 'b3', ' ', 'b4', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', 'w3', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b5', 'w3', ' ', ' ', ' ', ' ', ' ', 'b2', 'w2', ' '],
            [' ', ' ', ' ', 'b3', 'w2', 'b2', ' ', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b5', 'w3', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', 'b3', ' ', ' ', ' ', 'b5', ' ', ' ', ' ', ' ', ' ', 'w5'],
            ['w2', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', 'b4', ' ', 'w3', ' ', 'b4', ' ', ' ', 'b5', ' ', ' ', ' ', 'b6', ' ', 'b2', ' ', 'w3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', 'b5', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', 'b5', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', 'b4', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' '],
            [' ', ' ', 'b3', ' ', 'b6', ' ', ' ', ' ', ' ', ' ', ' ', 'w5', 'w3', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b7', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', 'b7', ' ', 'b3', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', 'b3', ' ', ' ', 'b3', 'w2', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' '],
            ['b3', 'b3', ' ', ' ', ' ', 'w5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', 'w2', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'b4', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', 'b5', 'b4', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', 'b5', ' ', ' ', 'b4', ' ', 'w5', ' ', ' ', ' ', ' ', 'b2', ' ', 'w8'],
            [' ', ' ', 'b5', 'w2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w4', ' ', 'w4', ' ', ' ', 'b3', ' ', ' ', 'b4', 'w2', ' ', ' ', ' ', ' ', 'b4', ' ', 'b2', ' ', ' ', 'w5', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'w5', ' ', ' ', ' ', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', 'b2', 'b3', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', 'b5', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', 'b5', ' ', ' ', 'b2', 'b2', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', 'b2', 'b3', ' ', ' ', 'w3', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', 'b6', 'b3', ' ', ' ', ' ', 'b5', ' ', ' ', 'b4', ' ', ' ', 'b5', ' ', 'b2', ' ', 'b2', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'b3', 'b4', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', 'b2', ' ', ' ', 'b3', 'b2', 'b3', 'w2', ' ', 'b5', ' '],
            [' ', ' ', ' ', ' ', 'w4', ' ', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', 'w4', 'b3', ' ', ' ', ' ', ' ', 'b3', 'w3', 'b3', ' ', 'w2', ' ', ' ', 'b5', ' ', 'b3', ' ', ' ', 'b2', 'b5', ' ', ' ', ' ', ' ', ' ', 'b2', 'b3', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w6', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', 'b2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w5', ' ', ' ', ' ', ' ', ' '],
            ['b5', 'w3', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w2', ' ', ' ', ' ', 'w2', 'b3', ' ', ' ', ' ', 'b4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b3', ' ', ' ', 'w6', ' ', ' ', ' ', ' ', ' ']
        ])
        game_solver = ShingokiSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution_string = (
            '    ┌────────┐  ┌───────────┐        ┌──┐  ┌─────┐     ┌────────┐  ┌──┐  ┌──┐        ┌──┐           ┌──┐  ┌──┐     ┌──┐    \n'
            ' ┌──┘  ┌─────┘  └──┐  ┌──┐  │  ┌─────┘  │  └──┐  │  ┌──┘  ┌──┐  │  │  └──┘  │  ┌──┐  │  └─────┐     │  └──┘  │     │  │    \n'
            ' │  ┌──┘     ┌─────┘  │  └──┘  └─────┐  │  ┌──┘  │  │  ┌──┘  │  │  │  ┌──┐  │  │  └──┘  ┌──┐  └─────┘  ┌─────┘     │  │    \n'
            ' │  │  ┌─────┘  ┌──┐  │  ┌──┐     ┌──┘  │  └──┐  │  │  │  ┌──┘  │  │  │  │  └──┘     ┌──┘  └───────────┘     ┌─────┘  └──┐ \n'
            ' │  │  │  ┌─────┘  │  │  │  │     └──┐  └─────┘  │  │  │  │  ┌──┘  └──┘  │  ┌─────┐  │  ┌────────────────────┘  ┌──┐  ┌──┘ \n'
            ' │  │  │  └──┐     │  │  │  └─────┐  └────────┐  └──┘  │  │  └────────┐  │  │     └──┘  └──┐  ┌─────┐  ┌─────┐  │  │  └──┐ \n'
            ' │  │  └──┐  │     └──┘  │  ┌──┐  └────────┐  └─────┐  │  └─────┐  ┌──┘  │  └─────┐        │  │     └──┘     │  │  └─────┘ \n'
            ' │  └──┐  │  │  ┌────────┘  │  └────────┐  │  ┌──┐  └──┘     ┌──┘  │  ┌──┘     ┌──┘     ┌──┘  │  ┌──┐        └──┘          \n'
            ' └──┐  │  │  │  └────────┐  └──┐  ┌─────┘  │  │  │     ┌──┐  │  ┌──┘  └─────┐  └────────┘  ┌──┘  │  └─────┐     ┌────────┐ \n'
            '    │  │  │  └──┐        └─────┘  │  ┌─────┘  │  └─────┘  │  │  │  ┌────────┘  ┌────────┐  └──┐  └─────┐  └─────┘  ┌─────┘ \n'
            '    │  │  └──┐  └──────────────┐  │  │        │  ┌─────┐  │  │  │  │  ┌────────┘        └─────┘  ┌──┐  │  ┌─────┐  │       \n'
            ' ┌──┘  │     └──────────────┐  │  │  └──┐     └──┘     │  │  │  └──┘  │     ┌──┐     ┌─────┐     │  │  │  └──┐  │  └─────┐ \n'
            ' │  ┌──┘  ┌─────────────────┘  │  └──┐  │  ┌──┐        │  │  └──┐  ┌──┘  ┌──┘  │     └──┐  │  ┌──┘  │  │  ┌──┘  └─────┐  │ \n'
            ' │  └──┐  │  ┌─────────────────┘     │  └──┘  │  ┌──┐  │  └──┐  │  │     └──┐  │  ┌─────┘  │  │  ┌──┘  │  │  ┌──┐     └──┘ \n'
            ' │  ┌──┘  │  │                 ┌──┐  └──┐  ┌──┘  │  │  │  ┌──┘  │  │     ┌──┘  │  │  ┌─────┘  │  │     │  │  │  └─────┐    \n'
            ' │  └──┐  │  │  ┌─────┐     ┌──┘  │  ┌──┘  └──┐  │  └──┘  └─────┘  └─────┘  ┌──┘  │  │     ┌──┘  └─────┘  │  │  ┌──┐  │    \n'
            ' └──┐  └──┘  │  └──┐  └─────┘  ┌──┘  │  ┌─────┘  └──┐  ┌──┐  ┌──────────────┘     │  │     │  ┌──┐  ┌──┐  │  │  │  │  │    \n'
            '    │  ┌─────┘     │  ┌─────┐  └──┐  │  └──┐  ┌─────┘  │  │  │     ┌──┐  ┌────────┘  └──┐  │  │  │  │  │  └──┘  │  │  │    \n'
            '    │  └────────┐  └──┘     └──┐  │  └──┐  │  └─────┐  │  │  └─────┘  └──┘  ┌──┐  ┌──┐  │  │  │  │  │  └─────┐  │  │  └──┐ \n'
            '    │  ┌─────┐  └──┐     ┌──┐  │  │     │  │        │  │  └─────┐  ┌────────┘  └──┘  └──┘  │  │  └──┘        └──┘  └──┐  │ \n'
            ' ┌──┘  │     └──┐  └──┐  │  │  │  │     │  │  ┌─────┘  │     ┌──┘  └────────┐  ┌────────┐  │  └─────┐  ┌────────┐     │  │ \n'
            ' └──┐  │        └──┐  │  │  └──┘  └──┐  │  │  │  ┌──┐  │     │  ┌────────┐  └──┘  ┌──┐  └──┘  ┌─────┘  │  ┌──┐  │  ┌──┘  │ \n'
            '    │  │     ┌──┐  │  └──┘  ┌─────┐  └──┘  │  └──┘  └──┘     │  │     ┌──┘  ┌─────┘  │  ┌─────┘     ┌──┘  │  │  └──┘  ┌──┘ \n'
            ' ┌──┘  │  ┌──┘  └──┘  ┌──┐  │     └──┐     └──┐  ┌────────┐  │  └──┐  └─────┘        │  │     ┌──┐  │  ┌──┘  │  ┌─────┘    \n'
            ' └─────┘  └───────────┘  │  │  ┌─────┘  ┌─────┘  │  ┌──┐  │  │  ┌──┘        ┌──┐  ┌──┘  │  ┌──┘  └──┘  │     └──┘     ┌──┐ \n'
            '             ┌──┐  ┌──┐  └──┘  │  ┌─────┘        │  │  │  │  │  │     ┌─────┘  │  │  ┌──┘  │  ┌────────┘        ┌──┐  │  │ \n'
            ' ┌──┐  ┌──┐  │  └──┘  │  ┌──┐  │  │        ┌─────┘  │  │  └──┘  │  ┌──┘  ┌──┐  │  │  │  ┌──┘  │        ┌────────┘  └──┘  │ \n'
            ' │  └──┘  │  └──┐  ┌──┘  │  └──┘  └────────┘  ┌─────┘  └────────┘  │  ┌──┘  │  │  └──┘  └──┐  └─────┐  │  ┌───────────┐  │ \n'
            ' └─────┐  └─────┘  └──┐  │  ┌──┐  ┌──┐  ┌──┐  └──┐     ┌──┐  ┌──┐  └──┘     │  │           └─────┐  │  └──┘     ┌─────┘  │ \n'
            ' ┌──┐  └─────┐  ┌──┐  │  │  │  │  │  │  │  └──┐  │  ┌──┘  └──┘  └───────────┘  └──┐  ┌──┐  ┌──┐  │  └──┐  ┌─────┘  ┌─────┘ \n'
            ' │  └──┐     │  │  │  │  └──┘  │  │  │  └──┐  │  │  │  ┌─────┐  ┌──┐  ┌──┐  ┌─────┘  │  └──┘  │  └──┐  │  │  ┌─────┘  ┌──┐ \n'
            ' └──┐  │     │  │  │  └──┐     │  │  └─────┘  │  │  │  │     │  │  └──┘  │  └──┐  ┌──┘  ┌──┐  │     │  │  │  │  ┌──┐  │  │ \n'
            '    │  │     │  │  └──┐  │  ┌──┘  │     ┌─────┘  └──┘  │     └──┘        └──┐  │  │  ┌──┘  │  └──┐  │  │  │  │  │  └──┘  │ \n'
            ' ┌──┘  └─────┘  │     │  │  │  ┌──┘     │  ┌───────────┘     ┌─────┐  ┌─────┘  │  │  │  ┌──┘  ┌──┘  │  │  │  │  │  ┌──┐  │ \n'
            ' └──────────────┘  ┌──┘  └──┘  │     ┌──┘  │        ┌──┐     └──┐  │  │  ┌─────┘  │  │  │  ┌──┘     │  └──┘  └──┘  │  │  │ \n'
            '    ┌────────┐     │  ┌────────┘     └──┐  └────────┘  │     ┌──┘  └──┘  └──┐  ┌──┘  │  │  └──┐     └─────┐  ┌─────┘  │  │ \n'
            ' ┌──┘  ┌──┐  └─────┘  │        ┌──┐     │  ┌────────┐  └──┐  └──┐  ┌────────┘  │  ┌──┘  └──┐  └──┐     ┌──┘  │  ┌──┐  │  │ \n'
            ' └─────┘  └────────┐  │  ┌─────┘  └──┐  │  │        │  ┌──┘  ┌──┘  │  ┌──┐     │  │        └──┐  └─────┘  ┌──┘  │  └──┘  │ \n'
            ' ┌──┐  ┌───────────┘  └──┘  ┌──┐  ┌──┘  │  └──┐     │  └──┐  │  ┌──┘  │  └─────┘  └──┐     ┌──┘  ┌────────┘     └──┐  ┌──┘ \n'
            ' │  └──┘  ┌─────────────────┘  │  └──┐  └──┐  └──┐  └──┐  │  │  │  ┌──┘  ┌────────┐  │     └──┐  │  ┌──────────────┘  │    \n'
            ' └────────┘                    └─────┘     └─────┘     └──┘  └──┘  └─────┘        └──┘        └──┘  └─────────────────┘    '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
