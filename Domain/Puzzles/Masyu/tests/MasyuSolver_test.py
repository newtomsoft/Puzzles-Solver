import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Masyu.MasyuSolver import MasyuSolver


class MasyuSolverTests(TestCase):
    def test_solution_white_0(self):
        grid = Grid([
            [' ', 'w', ' '],
            [' ', 'w', ' '],
        ])

        game_solver = MasyuSolver(grid)

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_1(self):
        grid = Grid([
            [' ', 'w', ' '],
            [' ', ' ', ' '],
            [' ', 'w', ' '],
        ])

        game_solver = MasyuSolver(grid)

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' │  ·  │ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_2(self):
        grid = Grid([
            [' ', 'w', ' ', ' '],
            ['w', ' ', ' ', 'w'],
            [' ', ' ', 'w', ' '],
        ])
        game_solver = MasyuSolver(grid)

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌────────┐ \n'
            ' │  ·  ·  │ \n'
            ' └────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black(self):
        grid = Grid([
            ['b', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', 'b'],
        ])
        game_solver = MasyuSolver(grid)

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' │  ·  │ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_basic_grid(self):
        grid = Grid([
            ['b', ' ', 'w', ' '],
            [' ', ' ', 'w', ' '],
            [' ', ' ', ' ', ' ']
        ])
        game_solver = MasyuSolver(grid)

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌────────┐ \n'
            ' │  ┌─────┘ \n'
            ' └──┘  ·  · '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_0(self):
        grid = Grid([
            ['b', 'w', ' ', ' ', ' ', ' '],
            ['w', ' ', ' ', 'w', 'w', ' '],
            [' ', 'b', 'w', ' ', ' ', ' '],
            [' ', 'w', ' ', ' ', ' ', 'b'],
            ['w', ' ', ' ', 'w', ' ', ' '],
            ['b', ' ', ' ', 'w', ' ', ' ']
        ])
        game_solver = MasyuSolver(grid)

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐  ·  ·  · \n'
            ' │  ·  └────────┐ \n'
            ' │  ┌─────┐  ·  │ \n'
            ' │  │  ·  └─────┘ \n'
            ' │  └────────┐  · \n'
            ' └───────────┘  · '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_1(self):
        grid = Grid([
            [' ', 'b', ' ', ' ', 'w', ' '],
            [' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'w', 'b', 'w', ' ', 'b'],
            [' ', ' ', ' ', ' ', ' ', 'b'],
            [' ', ' ', ' ', ' ', ' ', ' '],
            ['b', ' ', ' ', ' ', 'w', ' ']
        ])
        game_solver = MasyuSolver(grid)

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ·  ┌───────────┐ \n'
            ' ·  │  ·  ·  ·  │ \n'
            ' ·  │  ┌────────┘ \n'
            ' ┌──┘  │  ┌─────┐ \n'
            ' │  ·  └──┘  ·  │ \n'
            ' └──────────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_0(self):
        grid = Grid([
            ['b', 'w', ' ', 'w', ' ', ' ', 'w', ' '],
            ['w', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
            [' ', ' ', ' ', ' ', 'w', ' ', ' ', ' '],
            [' ', 'w', 'w', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', 'b', 'w', 'w', ' ', 'w'],
            [' ', ' ', 'w', ' ', ' ', ' ', ' ', ' '],
            ['b', 'w', ' ', ' ', 'w', 'w', ' ', ' '],
            [' ', ' ', ' ', ' ', 'w', ' ', 'w', 'b']
        ])
        game_solver = MasyuSolver(grid)

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌───────────┐  ┌─────┐ \n'
            ' │  ·  ·  ·  │  │  ·  │ \n'
            ' └──┐  ┌──┐  │  │  ┌──┘ \n'
            ' ·  │  │  │  └──┘  └──┐ \n'
            ' ┌──┘  │  └────────┐  │ \n'
            ' │  ·  │  ·  ·  ·  │  │ \n'
            ' └─────┘  ┌────────┘  │ \n'
            ' ·  ·  ·  └───────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_1(self):
        grid = Grid([
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b'],
            ['w', ' ', 'b', ' ', 'b', ' ', ' ', ' '],
            ['w', ' ', ' ', ' ', ' ', 'w', ' ', ' '],
            [' ', 'w', ' ', ' ', ' ', ' ', 'w', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['b', ' ', ' ', 'b', 'b', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', 'w', ' ', 'w', ' ', ' ', ' ', 'b']
        ])
        game_solver = MasyuSolver(grid)

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌────────────────────┐ \n'
            ' │  ·  ┌─────┐  ┌──┐  │ \n'
            ' │  ·  │  ·  │  │  └──┘ \n'
            ' └─────┘  ┌──┘  └─────┐ \n'
            ' ·  ·  ·  │  ·  ·  ·  │ \n'
            ' ┌────────┘  ┌─────┐  │ \n'
            ' │  ·  ·  ·  │  ┌──┘  │ \n'
            ' └───────────┘  └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_0(self):
        grid = Grid([
            [' ', ' ', 'b', 'w', ' ', ' ', ' ', ' ', ' ', 'b'],
            ['w', ' ', 'w', ' ', 'b', 'w', ' ', 'w', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'w', ' ', 'b', ' ', ' ', 'w', ' ', ' '],
            [' ', 'w', 'b', 'w', ' ', ' ', ' ', 'w', ' ', ' '],
            ['w', 'b', 'w', ' ', ' ', 'w', 'w', 'b', ' ', 'b'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b', ' '],
            [' ', ' ', 'w', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['w', ' ', ' ', ' ', 'b', 'w', 'w', ' ', ' ', ' '],
            ['b', 'w', 'b', 'b', ' ', ' ', ' ', ' ', 'w', ' ']
        ])
        game_solver = MasyuSolver(grid)

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  ┌────────────────────┐ \n'
            ' │  │  │  ·  ┌───────────┐  │ \n'
            ' │  │  │  ·  │  ·  ·  ┌──┘  │ \n'
            ' │  │  │  ·  └─────┐  │  ·  │ \n'
            ' │  │  └────────┐  │  │  ·  │ \n'
            ' │  └────────┐  │  │  └─────┘ \n'
            ' └──┐  ┌──┐  │  │  └─────┐  · \n'
            ' ┌──┘  │  │  │  └─────┐  │  · \n'
            ' │  ·  │  │  └────────┘  └──┐ \n'
            ' └─────┘  └─────────────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_1(self):
        grid = Grid([
            [' ', ' ', 'b', 'w', ' ', ' ', 'b', 'b', ' ', ' '],
            [' ', ' ', 'w', ' ', ' ', ' ', 'w', 'w', ' ', 'w'],
            ['w', ' ', ' ', ' ', 'w', ' ', 'w', 'w', ' ', 'w'],
            [' ', 'w', 'w', ' ', 'w', 'w', ' ', ' ', ' ', ' '],
            ['w', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w', ' '],
            [' ', ' ', 'b', 'w', 'b', ' ', ' ', ' ', 'w', ' '],
            [' ', ' ', 'w', ' ', ' ', ' ', ' ', 'w', ' ', ' '],
            [' ', 'w', 'w', ' ', ' ', 'w', ' ', ' ', ' ', 'w'],
            [' ', ' ', ' ', 'w', 'w', ' ', 'w', ' ', ' ', 'w'],
            [' ', ' ', ' ', 'b', ' ', 'w', ' ', ' ', 'w', 'b']
        ])
        game_solver = MasyuSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ·  ·  ┌───────────┐  ┌─────┐ \n'
            ' ┌──┐  │  ·  ┌──┐  │  │  ·  │ \n'
            ' │  │  │  ·  │  │  │  │  ·  │ \n'
            ' │  │  │  ·  │  │  └──┘  ┌──┘ \n'
            ' │  └──┘  ┌──┘  └─────┐  │  · \n'
            ' └─────┐  │  ┌─────┐  │  │  · \n'
            ' ┌──┐  │  │  │  ┌──┘  │  └──┐ \n'
            ' │  │  │  │  │  │  ·  └──┐  │ \n'
            ' │  └──┘  │  │  └────────┘  │ \n'
            ' └────────┘  └──────────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_2(self):
        grid = Grid([
            [' ', ' ', ' ', ' ', 'w', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w', ' ', ' '],
            ['w', 'b', ' ', 'b', ' ', 'b', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'b', 'w', ' ', ' '],
            [' ', ' ', ' ', 'w', ' ', 'b', ' ', ' ', ' ', 'w'],
            [' ', 'b', ' ', 'b', ' ', 'w', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w', ' ', ' '],
            [' ', ' ', ' ', ' ', 'w', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', 'w', ' ', 'w', ' ', 'w', ' ', ' '],
            [' ', ' ', 'b', ' ', ' ', ' ', 'w', ' ', 'w', ' ']
        ])
        game_solver = MasyuSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  ·  ┌─────┐  ┌────────┐ \n'
            ' │  │  ·  │  ·  │  └─────┐  │ \n'
            ' │  └─────┘  ·  └─────┐  │  │ \n'
            ' └──┐  ┌───────────┐  │  │  │ \n'
            ' ┌──┘  └────────┐  │  └──┘  │ \n'
            ' │  ┌─────┐  ·  │  └──┐  ┌──┘ \n'
            ' │  │  ·  │  ┌──┘  ·  │  └──┐ \n'
            ' │  └──┐  │  │  ┌──┐  └──┐  │ \n'
            ' │  ·  │  │  │  │  └─────┘  │ \n'
            ' └─────┘  └──┘  └───────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15(self):
        grid = Grid([
            [' ', ' ', ' ', ' ', 'w', ' ', ' ', 'w', ' ', ' ', ' ', ' ', 'w', 'b', ' '],
            [' ', 'w', ' ', 'w', ' ', ' ', ' ', ' ', 'w', 'w', 'b', ' ', ' ', 'w', ' '],
            [' ', 'b', ' ', ' ', ' ', 'w', 'w', ' ', ' ', ' ', ' ', 'b', ' ', ' ', ' '],
            [' ', ' ', 'b', 'w', ' ', ' ', 'w', ' ', ' ', ' ', 'b', ' ', 'b', ' ', 'b'],
            [' ', 'w', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w'],
            [' ', 'w', ' ', ' ', ' ', 'w', ' ', ' ', 'w', 'w', ' ', 'w', ' ', ' ', ' '],
            [' ', 'b', 'w', ' ', ' ', ' ', ' ', ' ', ' ', 'w', ' ', ' ', ' ', ' ', ' '],
            [' ', 'w', 'w', ' ', 'w', 'w', 'w', ' ', ' ', ' ', ' ', ' ', 'w', 'b', 'w'],
            ['w', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w', 'w', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', 'w', 'w', ' ', ' ', 'b', ' ', 'b', ' ', 'w', ' ', ' ', 'w'],
            [' ', ' ', ' ', 'w', ' ', 'b', ' ', 'b', 'w', 'w', 'b', 'w', ' ', 'w', ' '],
            ['b', 'w', ' ', 'w', 'b', 'w', 'w', ' ', ' ', ' ', ' ', ' ', ' ', 'w', ' '],
            ['b', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w', 'w', ' ', ' ', ' ', ' '],
            ['w', ' ', ' ', 'w', ' ', ' ', 'w', 'w', ' ', 'w', ' ', ' ', 'w', 'w', 'w'],
            [' ', ' ', ' ', ' ', 'w', ' ', ' ', ' ', ' ', ' ', 'b', 'w', 'b', ' ', ' ']
        ])

        game_solver = MasyuSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  ·  ┌─────┐  ┌────────────────────┐  · \n'
            ' │  │  ·  │  ·  └──┘  ┌────────┐  ·  ·  │  · \n'
            ' │  └─────┘  ┌────────┘  ·  ·  │  ┌─────┘  · \n'
            ' └──┐  ┌─────┘  ┌──────────────┘  │  ┌─────┐ \n'
            ' ·  │  │  ·  ┌──┘  ┌──┐  ·  ·  ·  │  │  ·  │ \n'
            ' ·  │  └──┐  └─────┘  └────────┐  │  │  ┌──┘ \n'
            ' ·  └─────┘  ┌──┐  ┌──┐  ┌─────┘  └──┘  └──┐ \n'
            ' ┌────────┐  │  │  │  │  └──┐  ┌────────┐  │ \n'
            ' │  ·  ·  └──┘  │  │  │  ·  │  │  ┌──┐  │  │ \n'
            ' │  ·  ┌────────┘  │  └─────┘  │  │  └──┘  │ \n'
            ' │  ·  └────────┐  │  ┌────────┘  │  ┌─────┘ \n'
            ' └───────────┐  │  │  │  ┌──┐  ┌──┘  └─────┐ \n'
            ' ┌─────┐  ·  │  └──┘  └──┘  │  │  ·  ┌──┐  │ \n'
            ' │  ·  └─────┘  ┌────────┐  │  │  ·  │  │  │ \n'
            ' └──────────────┘  ·  ·  └──┘  └─────┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    # @unittest.skip("Skipping because it takes too long approximately 8 seconds")
    def test_solution_20x20(self):
        grid = Grid([
            [' ', 'w', ' ', 'w', ' ', ' ', 'b', 'w', 'w', ' ', ' ', ' ', ' ', ' ', ' ', 'w', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', 'w', ' ', ' ', ' ', ' ', 'w', ' ', 'w', ' ', ' ', 'b', 'w', ' ', ' ', ' ', ' ', 'w'],
            ['w', ' ', 'w', ' ', ' ', ' ', ' ', 'w', ' ', ' ', ' ', 'w', ' ', ' ', ' ', 'w', 'w', 'w', 'w', ' '],
            [' ', 'w', ' ', 'w', 'b', 'w', ' ', ' ', ' ', ' ', ' ', 'w', ' ', ' ', 'w', ' ', ' ', 'w', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'w', 'w', 'w', 'w', ' ', 'w', ' ', ' ', ' ', 'w', ' ', ' ', 'w', ' '],
            [' ', ' ', ' ', 'b', 'w', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w', ' ', ' ', 'b', ' ', 'b', ' '],
            ['w', ' ', ' ', ' ', 'b', 'w', ' ', ' ', ' ', 'b', ' ', ' ', ' ', ' ', 'w', ' ', 'w', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', 'w', ' ', ' ', 'w', ' ', ' ', 'w', 'w', ' ', ' ', ' ', ' ', 'w', 'w', 'w', ' '],
            ['w', 'w', 'b', ' ', 'w', ' ', 'b', 'w', 'w', ' ', 'b', 'w', 'w', ' ', 'w', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'w', ' ', ' ', ' ', ' ', ' ', 'w', ' ', ' ', 'w', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b', ' ', 'b', ' ', ' ', 'w', 'b', 'w', 'b', ' ', 'w', ' ', ' '],
            [' ', 'w', 'w', 'b', ' ', 'w', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w', ' ', ' ', ' ', 'w', 'w', ' '],
            [' ', ' ', ' ', 'w', 'b', ' ', ' ', ' ', ' ', ' ', ' ', 'w', 'w', 'b', 'w', ' ', 'w', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', 'w', 'b', ' ', 'w', ' ', 'w', 'w', ' ', ' ', ' ', ' ', ' ', ' ', 'w', ' ', ' '],
            ['w', 'b', 'w', 'w', ' ', ' ', ' ', ' ', ' ', ' ', 'w', 'b', 'w', ' ', 'w', ' ', 'w', ' ', 'w', ' '],
            [' ', 'w', ' ', ' ', ' ', 'w', ' ', ' ', ' ', 'w', 'b', 'w', ' ', ' ', 'b', 'w', ' ', 'b', ' ', ' '],
            ['w', ' ', 'w', ' ', ' ', 'b', 'w', ' ', ' ', ' ', ' ', 'w', ' ', ' ', ' ', ' ', ' ', ' ', 'w', ' '],
            ['b', ' ', ' ', 'w', 'b', ' ', 'w', ' ', 'w', ' ', ' ', 'b', ' ', ' ', ' ', ' ', 'w', 'b', ' ', ' '],
            [' ', ' ', ' ', ' ', 'w', ' ', ' ', 'w', 'b', 'w', 'b', ' ', ' ', ' ', 'b', ' ', ' ', ' ', ' ', 'w'],
            [' ', ' ', 'w', ' ', 'w', ' ', ' ', 'b', 'w', ' ', 'w', ' ', ' ', ' ', ' ', 'b', ' ', ' ', 'w', 'b']
        ])
        game_solver = MasyuSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌───────────┐  ·  ┌────────┐  ┌──┐  ·  ·  ┌──────────────┐ \n'
            ' │  ┌────────┘  ·  │  ┌─────┘  │  └─────┐  │  ┌──┐  ┌──┐  │ \n'
            ' │  └───────────┐  │  │  ·  ·  └─────┐  │  │  │  │  │  │  │ \n'
            ' └───────────┐  │  │  │  ┌──┐  ┌─────┘  │  │  │  │  │  │  │ \n'
            ' ·  ·  ·  ·  │  │  │  │  │  │  └─────┐  └──┘  │  └──┘  │  │ \n'
            ' ┌────────┐  │  └──┘  └──┘  │  ·  ·  └────────┘  ┌─────┘  │ \n'
            ' │  ┌──┐  │  └───────────┐  └────────┐  ┌─────┐  │  ┌──┐  │ \n'
            ' │  │  │  └──────────────┘  ┌────────┘  └──┐  │  │  │  │  │ \n'
            ' │  │  └────────┐  ┌────────┘  ┌────────┐  │  │  └──┘  │  │ \n'
            ' └──┘  ·  ┌─────┘  │  ·  ·  ·  │  ┌─────┘  │  │  ·  ·  │  │ \n'
            ' ·  ·  ·  │  ┌──┐  │  ┌─────┐  │  └─────┐  │  └────────┘  │ \n'
            ' ┌────────┘  │  │  │  │  ·  │  │  ┌──┐  │  └──┐  ┌────────┘ \n'
            ' └──┐  ┌─────┘  └──┘  │  ·  └──┘  │  │  └─────┘  │  ┌─────┐ \n'
            ' ┌──┘  └────────┐  ·  │  ┌────────┘  │  ┌──┐  ┌──┘  │  ┌──┘ \n'
            ' │  ┌────────┐  │  ┌──┘  └────────┐  │  │  │  └─────┘  │  · \n'
            ' │  │  ·  ·  │  │  └───────────┐  │  └──┘  └────────┐  │  · \n'
            ' │  └─────┐  │  └────────┐  ·  │  │  ·  ┌──┐  ·  ·  │  │  · \n'
            ' └─────┐  │  └────────┐  │  ·  │  └─────┘  │  ┌─────┘  └──┐ \n'
            ' ·  ┌──┘  └─────┐  ·  │  └─────┘  ┌────────┘  │  ·  ·  ·  │ \n'
            ' ·  └───────────┘  ·  └───────────┘  ·  ·  ·  └───────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
