import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Shingoki.ShingokiSolver import ShingokiSolver

# region
__ = ' '
W0 = 'w0'
W2 = 'w2'
W3 = 'w3'
W4 = 'w4'
B0 = 'b0'
B2 = 'b2'
B3 = 'b3'
B4 = 'b4'
B5 = 'b5'
B6 = 'b6'
B7 = 'b7'
B8 = 'b8'
G0 = 'g0'
G2 = 'g2'
G3 = 'g3'
G4 = 'g4'
G5 = 'g5'
G6 = 'g6'
G7 = 'g7'
# endregion

class ShingokiWithGrayCirclesSolverTests(TestCase):
    def test_solution_7x7(self):

        grid = Grid([
            [__, B2, __, __, __, G3, __],
            [W2, __, __, __, __, __, B6],
            [__, __, __, __, __, __, __],
            [__, W2, __, B3, __, B4, __],
            [__, __, __, __, __, __, __],
            [__, __, __, __, __, __, __],
            [__, B2, __, G2, __, G4, __],
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  ·  ┌─────┐  · \n'
            ' │  └─────┘  ·  └──┐ \n'
            ' └──┐  ┌─────┐  ·  │ \n'
            ' ·  │  └──┐  └──┐  │ \n'
            ' ┌──┘  ·  │  ·  │  │ \n'
            ' │  ┌──┐  └──┐  │  │ \n'
            ' └──┘  └─────┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12(self):
        grid = Grid([
            [__, __, __, __, G3, __, __, __, __, __, W2, __],
            [__, B2, __, __, __, __, W2, __, __, __, __, __],
            [__, __, __, G2, G3, G2, __, W3, __, __, __, __],
            [G4, __, B2, __, __, __, __, __, __, __, __, __],
            [__, __, __, __, __, __, __, W2, __, __, __, G7],
            [__, W2, __, B3, __, __, B2, __, __, __, __, __],
            [__, __, __, __, __, B4, __, __, __, G4, __, __],
            [__, __, __, B5, __, __, __, __, B4, __, G2, W2],
            [__, __, B4, __, __, __, __, __, __, G2, __, __],
            [W4, __, __, __, __, __, W2, __, G2, __, B2, __],
            [__, __, __, __, B2, __, __, B2, __, __, __, __],
            [__, __, W3, __, __, __, __, __, B3, __, __, __],
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ·  ┌──┐  ┌──┐  ·  ·  ┌──┐  ┌─────┐ \n'
            ' ┌──┘  └──┘  │  ┌─────┘  └──┘  ·  │ \n'
            ' │  ·  ┌──┐  └──┘  ┌────────┐  ·  │ \n'
            ' │  ┌──┘  └─────┐  └──┐  ┌──┘  ·  │ \n'
            ' │  └──┐  ·  ·  │  ·  │  └────────┘ \n'
            ' └─────┘  ┌──┐  │  ┌──┘  ·  ·  ·  · \n'
            ' ·  ·  ·  │  └──┘  └────────┐  ┌──┐ \n'
            ' ┌────────┘  ·  ┌────────┐  └──┘  │ \n'
            ' │  ·  ┌────────┘  ┌──┐  └──┐  ┌──┘ \n'
            ' │  ·  └─────┐  ·  │  └─────┘  └──┐ \n'
            ' │  ·  ·  ┌──┘  ┌──┘  ┌──┐  ·  ┌──┘ \n'
            ' └────────┘  ·  └─────┘  └─────┘  · '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_white_undefined_segment_len(self):
        grid = Grid([
            [__, __, __, __, B8],
            [__, __, B3, __, __],
            [__, __, __, __, __],
            [__, __, W0, __, __],
            [__, B4, __, __, __]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌───────────┐ \n'
            ' └─────┐  ·  │ \n'
            ' ·  ·  └──┐  │ \n'
            ' ·  ┌─────┘  │ \n'
            ' ·  └────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_black_undefined_segment_len(self):
        grid = Grid([
            [__, __, W4, __, __, B0],
            [__, __, __, __, __, __],
            [G3, __, __, B3, __, __],
            [__, __, W2, __, __, B2],
            [__, __, __, __, B0, __],
            [B6, __, __, __, __, __]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ·  ┌───────────┐ \n'
            ' ┌──┘  ·  ┌─────┘ \n'
            ' └─────┐  └─────┐ \n'
            ' ·  ·  │  ·  ┌──┘ \n'
            ' ┌─────┘  ·  └──┐ \n'
            ' └──────────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_gray_undefined_segment_len(self):
        grid = Grid([
            [__, G3, __, __, __, __],
            [G5, __, __, __, __, W4],
            [__, __, __, __, B3, __],
            [__, G4, __, __, __, __],
            [__, __, G0, __, __, __],
            [B5, __, __, __, __, __]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ·  ┌─────┐  ┌──┐ \n'
            ' ┌──┘  ·  │  │  │ \n'
            ' │  ·  ·  └──┘  │ \n'
            ' │  ┌─────┐  ·  │ \n'
            ' │  │  ┌──┘  ┌──┘ \n'
            ' └──┘  └─────┘  · '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_white_and_black_undefined_segment_len(self):
        grid = Grid([
            [__, __, B3, __, __],
            [__, __, __, __, __],
            [B0, __, __, __, G3],
            [__, W0, __, W0, __],
            [__, __, B3, __, __]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐  ·  · \n'
            ' │  ·  └─────┐ \n'
            ' └──┐  ┌──┐  │ \n'
            ' ·  │  │  │  │ \n'
            ' ·  └──┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_white_and_black_undefined_segment_len(self):
        grid = Grid([
            [__, __, W2, __, __, __],
            [__, __, __, __, __, G3],
            [__, B2, __, __, W0, __],
            [__, __, W0, __, __, __],
            [__, W0, __, __, W0, __],
            [__, __, __, __, __, B0]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ·  ┌─────┐  ·  · \n'
            ' ┌──┘  ·  └─────┐ \n'
            ' │  ┌──┐  ┌─────┘ \n'
            ' └──┘  │  │  ·  · \n'
            ' ┌─────┘  └─────┐ \n'
            ' └──────────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_all_colors_undefined_segment_len(self):
        grid = Grid([
            [__, __, __, G4, G4, __, __, __],
            [W0, __, __, __, __, __, __, B3],
            [__, __, __, G3, B0, __, __, __],
            [G3, __, __, __, __, __, __, G0],
            [__, __, __, W0, W0, __, __, __],
            [__, W2, __, __, __, __, G0, __],
            [__, __, __, G3, G0, __, __, __],
            [B0, __, __, __, __, __, __, B6]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  ┌──┐  ┌─────┐  · \n'
            ' │  └──┘  │  │  ·  └──┐ \n'
            ' └─────┐  │  └──┐  ·  │ \n'
            ' ┌─────┘  └─────┘  ┌──┘ \n'
            ' └──┐  ┌────────┐  │  · \n'
            ' ·  │  │  ·  ·  │  └──┐ \n'
            ' ┌──┘  │  ┌─────┘  ·  │ \n'
            ' └─────┘  └───────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12_all_colors_undefined_segment_len(self):
        grid = Grid([
            [B8, __, G0, __, __, __, __, __, __, G3, __, B7],
            [__, __, __, __, __, W2, W0, __, __, __, __, __],
            [__, __, __, W0, __, __, __, __, B0, __, __, __],
            [__, __, B6, __, __, __, __, __, __, W0, __, __],
            [__, W0, __, __, __, __, __, __, __, __, W0, __],
            [__, __, __, B5, __, __, __, __, B5, __, __, __],
            [W2, __, __, __, __, W0, G7, __, __, __, __, W2],
            [__, __, W0, __, __, __, __, __, __, B2, __, __],
            [__, __, __, __, __, __, __, __, __, __, __, __],
            [__, __, __, __, W3, __, __, B2, __, __, __, __],
            [G4, W3, __, __, __, __, __, __, __, __, G4, G0],
            [__, __, __, __, __, G4, G6, __, __, __, __, __]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──────────────┐  ┌──┐  ┌────────┐ \n'
            ' │  ·  ·  ·  ·  │  │  └──┘  ·  ·  │ \n'
            ' │  ·  ┌────────┘  └──┐  ┌──┐  ·  │ \n'
            ' └──┐  └──────────────┘  │  │  ·  │ \n'
            ' ·  │  ·  ┌──────────────┘  └─────┘ \n'
            ' ┌──┘  ·  └───────────┐  ┌────────┐ \n'
            ' │  ·  ┌───────────┐  │  │  ·  ·  │ \n'
            ' └──┐  │  ·  ·  ·  │  │  └──┐  ┌──┘ \n'
            ' ·  │  │  ·  ·  ·  │  └─────┘  │  · \n'
            ' ┌──┘  └────────┐  └──┐  ·  ·  │  · \n'
            ' └────────┐  ·  │  ┌──┘  ·  ·  └──┐ \n'
            ' ·  ·  ·  └─────┘  └──────────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()