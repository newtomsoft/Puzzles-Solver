import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Shingoki.ShingokiSolver import ShingokiSolver

____ = ' '


class ShingokiWithGrayCirclesSolverTests(TestCase):


    def test_solution_7x7(self):
        grid = Grid([
            [____, 'b2', ____, ____, ____, 'g3', ____],
            ['w2', ____, ____, ____, ____, ____, 'b6'],
            [____, ____, ____, ____, ____, ____, ____],
            [____, 'w2', ____, 'b3', ____, 'b4', ____],
            [____, ____, ____, ____, ____, ____, ____],
            [____, ____, ____, ____, ____, ____, ____],
            [____, 'b2', ____, 'g2', ____, 'g4', ____],
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐     ┌─────┐    \n'
            ' │  └─────┘     └──┐ \n'
            ' └──┐  ┌─────┐     │ \n'
            '    │  └──┐  └──┐  │ \n'
            ' ┌──┘     │     │  │ \n'
            ' │  ┌──┐  └──┐  │  │ \n'
            ' └──┘  └─────┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12(self):
        grid = Grid([
            [____, ____, ____, ____, 'g3', ____, ____, ____, ____, ____, 'w2', ____],
            [____, 'b2', ____, ____, ____, ____, 'w2', ____, ____, ____, ____, ____],
            [____, ____, ____, 'g2', 'g3', 'g2', ____, 'w3', ____, ____, ____, ____],
            ['g4', ____, 'b2', ____, ____, ____, ____, ____, ____, ____, ____, ____],
            [____, ____, ____, ____, ____, ____, ____, 'w2', ____, ____, ____, 'g7'],
            [____, 'w2', ____, 'b3', ____, ____, 'b2', ____, ____, ____, ____, ____],
            [____, ____, ____, ____, ____, 'b4', ____, ____, ____, 'g4', ____, ____],
            [____, ____, ____, 'b5', ____, ____, ____, ____, 'b4', ____, 'g2', 'w2'],
            [____, ____, 'b4', ____, ____, ____, ____, ____, ____, 'g2', ____, ____],
            ['w4', ____, ____, ____, ____, ____, 'w2', ____, 'g2', ____, 'b2', ____],
            [____, ____, ____, ____, 'b2', ____, ____, 'b2', ____, ____, ____, ____],
            [____, ____, 'w3', ____, ____, ____, ____, ____, 'b3', ____, ____, ____],
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            '    ┌──┐  ┌──┐        ┌──┐  ┌─────┐ \n'
            ' ┌──┘  └──┘  │  ┌─────┘  └──┘     │ \n'
            ' │     ┌──┐  └──┘  ┌────────┐     │ \n'
            ' │  ┌──┘  └─────┐  └──┐  ┌──┘     │ \n'
            ' │  └──┐        │     │  └────────┘ \n'
            ' └─────┘  ┌──┐  │  ┌──┘             \n'
            '          │  └──┘  └────────┐  ┌──┐ \n'
            ' ┌────────┘     ┌────────┐  └──┘  │ \n'
            ' │     ┌────────┘  ┌──┐  └──┐  ┌──┘ \n'
            ' │     └─────┐     │  └─────┘  └──┐ \n'
            ' │        ┌──┘  ┌──┘  ┌──┐     ┌──┘ \n'
            ' └────────┘     └─────┘  └─────┘    '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_white_undefined_segment_len(self):
        grid = Grid([
            [____, ____, ____, ____, 'b8'],
            [____, ____, 'b3', ____, ____],
            [____, ____, ____, ____, ____],
            [____, ____, 'w0', ____, ____],
            [____, 'b4', ____, ____, ____]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌───────────┐ \n'
            ' └─────┐     │ \n'
            '       └──┐  │ \n'
            '    ┌─────┘  │ \n'
            '    └────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_black_undefined_segment_len(self):
        grid = Grid([
            [____, ____, 'w4', ____, ____, 'b0'],
            [____, ____, ____, ____, ____, ____],
            ['g3', ____, ____, 'b3', ____, ____],
            [____, ____, 'w2', ____, ____, 'b2'],
            [____, ____, ____, ____, 'b0', ____],
            ['b6', ____, ____, ____, ____, ____]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            '    ┌───────────┐ \n'
            ' ┌──┘     ┌─────┘ \n'
            ' └─────┐  └─────┐ \n'
            '       │     ┌──┘ \n'
            ' ┌─────┘     └──┐ \n'
            ' └──────────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_gray_undefined_segment_len(self):
        grid = Grid([
            [____, 'g3', ____, ____, ____, ____],
            ['g5', ____, ____, ____, ____, 'w4'],
            [____, ____, ____, ____, 'b3', ____],
            [____, 'g4', ____, ____, ____, ____],
            [____, ____, 'g0', ____, ____, ____],
            ['b5', ____, ____, ____, ____, ____]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            '    ┌─────┐  ┌──┐ \n'
            ' ┌──┘     │  │  │ \n'
            ' │        └──┘  │ \n'
            ' │  ┌─────┐     │ \n'
            ' │  │  ┌──┘  ┌──┘ \n'
            ' └──┘  └─────┘    '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_white_and_black_undefined_segment_len(self):
        grid = Grid([
            [____, ____, 'b3', ____, ____],
            [____, ____, ____, ____, ____],
            ['b0', ____, ____, ____, 'g3'],
            [____, 'w0', ____, 'w0', ____],
            [____, ____, 'b3', ____, ____]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐       \n'
            ' │     └─────┐ \n'
            ' └──┐  ┌──┐  │ \n'
            '    │  │  │  │ \n'
            '    └──┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_white_and_black_undefined_segment_len(self):
        grid = Grid([
            [____, ____, 'w2', ____, ____, ____],
            [____, ____, ____, ____, ____, 'g3'],
            [____, 'b2', ____, ____, 'w0', ____],
            [____, ____, 'w0', ____, ____, ____],
            [____, 'w0', ____, ____, 'w0', ____],
            [____, ____, ____, ____, ____, 'b0']
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            '    ┌─────┐       \n'
            ' ┌──┘     └─────┐ \n'
            ' │  ┌──┐  ┌─────┘ \n'
            ' └──┘  │  │       \n'
            ' ┌─────┘  └─────┐ \n'
            ' └──────────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_all_colors_undefined_segment_len(self):
        grid = Grid([
            [____, ____, ____, 'g4', 'g4', ____, ____, ____],
            ['w0', ____, ____, ____, ____, ____, ____, 'b3'],
            [____, ____, ____, 'g3', 'b0', ____, ____, ____],
            ['g3', ____, ____, ____, ____, ____, ____, 'g0'],
            [____, ____, ____, 'w0', 'w0', ____, ____, ____],
            [____, 'w2', ____, ____, ____, ____, 'g0', ____],
            [____, ____, ____, 'g3', 'g0', ____, ____, ____],
            ['b0', ____, ____, ____, ____, ____, ____, 'b6']
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  ┌──┐  ┌─────┐    \n'
            ' │  └──┘  │  │     └──┐ \n'
            ' └─────┐  │  └──┐     │ \n'
            ' ┌─────┘  └─────┘  ┌──┘ \n'
            ' └──┐  ┌────────┐  │    \n'
            '    │  │        │  └──┐ \n'
            ' ┌──┘  │  ┌─────┘     │ \n'
            ' └─────┘  └───────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12_all_colors_undefined_segment_len(self):
        grid = Grid([
            ['b8', ____, 'g0', ____, ____, ____, ____, ____, ____, 'g3', ____, 'b7'],
            [____, ____, ____, ____, ____, 'w2', 'w0', ____, ____, ____, ____, ____],
            [____, ____, ____, 'w0', ____, ____, ____, ____, 'b0', ____, ____, ____],
            [____, ____, 'b6', ____, ____, ____, ____, ____, ____, 'w0', ____, ____],
            [____, 'w0', ____, ____, ____, ____, ____, ____, ____, ____, 'w0', ____],
            [____, ____, ____, 'b5', ____, ____, ____, ____, 'b5', ____, ____, ____],
            ['w2', ____, ____, ____, ____, 'w0', 'g7', ____, ____, ____, ____, 'w2'],
            [____, ____, 'w0', ____, ____, ____, ____, ____, ____, 'b2', ____, ____],
            [____, ____, ____, ____, ____, ____, ____, ____, ____, ____, ____, ____],
            [____, ____, ____, ____, 'w3', ____, ____, 'b2', ____, ____, ____, ____],
            ['g4', 'w3', ____, ____, ____, ____, ____, ____, ____, ____, 'g4', 'g0'],
            [____, ____, ____, ____, ____, 'g4', 'g6', ____, ____, ____, ____, ____]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──────────────┐  ┌──┐  ┌────────┐ \n'
            ' │              │  │  └──┘        │ \n'
            ' │     ┌────────┘  └──┐  ┌──┐     │ \n'
            ' └──┐  └──────────────┘  │  │     │ \n'
            '    │     ┌──────────────┘  └─────┘ \n'
            ' ┌──┘     └───────────┐  ┌────────┐ \n'
            ' │     ┌───────────┐  │  │        │ \n'
            ' └──┐  │           │  │  └──┐  ┌──┘ \n'
            '    │  │           │  └─────┘  │    \n'
            ' ┌──┘  └────────┐  └──┐        │    \n'
            ' └────────┐     │  ┌──┘        └──┐ \n'
            '          └─────┘  └──────────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()