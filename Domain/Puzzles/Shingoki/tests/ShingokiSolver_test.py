import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Shingoki.ShingokiSolver import ShingokiSolver

# region
__ = ' '
W1 = 'w1'
W2 = 'w2'
W3 = 'w3'
W4 = 'w4'
W5 = 'w5'
W6 = 'w6'
W7 = 'w7'
W8 = 'w8'
W9 = 'w9'
WB = 'w11'
WD = 'w13'
WF = 'w15'
B1 = 'b1'
B2 = 'b2'
B3 = 'b3'
B4 = 'b4'
B5 = 'b5'
B6 = 'b6'
B7 = 'b7'
B8 = 'b8'
B9 = 'b9'
BA = 'b10'
BE = 'b14'
BG = 'b16'
BH = 'b17'
# endregion


class ShingokiSolverTests(TestCase):
    def test_black2_not_loop(self):
        grid = Grid([
            [B2, __],
            [__, __]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_white_horizontal_w2(self):
        grid = Grid([
            [__, W2, __],
            [__, W2, __],
        ])
        game_solver = ShingokiSolver(grid)
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
            [__, __, W3, __],
            [__, W3, __, __],
        ])
        game_solver = ShingokiSolver(grid)
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
            [__, __],
            [W2, W2],
            [__, __],
        ])
        game_solver = ShingokiSolver(grid)
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
            [__, __],
            [W3, __],
            [__, W3],
            [__, __],
        ])
        game_solver = ShingokiSolver(grid)
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
            [__, W2, __],
            [W2, __, __],
            [__, W2, __]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' │  ·  │ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_horizontal_vertical_1(self):
        grid = Grid([
            [__, W3, __, __],
            [W3, __, __, W2],
            [__, __, __, __],
            [__, W2, __, __]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌────────┐ \n'
            ' │  ·  ·  │ \n'
            ' │  ·  ┌──┘ \n'
            ' └─────┘  · '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_horizontal_vertical_2(self):
        grid = Grid([
            [__, W3, __, __],
            [W3, __, __, __],
            [__, __, W2, __],
            [__, W2, __, __]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌────────┐ \n'
            ' │  ·  ┌──┘ \n'
            ' │  ·  │  · \n'
            ' └─────┘  · '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_right_down_b2_4(self):
        grid = Grid([
            [__, B2, __],
            [B2, __, __],
            [__, __, B4],
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ·  ┌──┐ \n'
            ' ┌──┘  │ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_right_down_b3(self):
        grid = Grid([
            [__, B3, __, __],
            [B3, __, __, __],
            [__, B3, __, __],
            [__, __, __, __],
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ·  ┌─────┐ \n'
            ' ┌──┘  ·  │ \n'
            ' │  ┌─────┘ \n'
            ' └──┘  ·  · '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_right_up_b2_4(self):
        grid = Grid([
            [__, __, B4],
            [B2, __, __],
            [__, B2, __],
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' └──┐  │ \n'
            ' ·  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_right_up_b3(self):
        grid = Grid([
            [__, __, __, __],
            [__, __, __, __],
            [B3, __, B3, __],
            [__, B3, __, __],
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐  · \n'
            ' │  ·  │  · \n'
            ' └──┐  └──┐ \n'
            ' ·  └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_left_down_b2_4(self):
        grid = Grid([
            [__, B2, __],
            [__, __, B2],
            [B4, __, __],
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  · \n'
            ' │  └──┐ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_left_down_b3(self):
        grid = Grid([
            [__, __, B3, __],
            [__, B3, __, B3],
            [__, __, __, __],
            [__, __, __, __],
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐  · \n'
            ' └──┐  └──┐ \n'
            ' ·  │  ·  │ \n'
            ' ·  └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_black_left_up_b2_4(self):
        grid = Grid([
            [B4, __, __],
            [__, __, B2],
            [__, B2, __],
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' │  ┌──┘ \n'
            ' └──┘  · '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_white_black(self):
        grid = Grid([
            [__, W2, __],
            [__, __, B2],
            [__, __, __],
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' │  ┌──┘ \n'
            ' └──┘  · '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_0(self):
        grid = Grid([
            [__, __, __, __, __, __],
            [B5, __, W2, __, __, __],
            [__, __, __, W4, __, B2],
            [__, __, __, __, __, __],
            [__, __, __, B6, __, B2],
            [__, W4, __, __, __, __],
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ·  ┌──┐  ┌──┐  · \n'
            ' ┌──┘  │  │  └──┐ \n'
            ' │  ┌──┘  │  ┌──┘ \n'
            ' │  │  ·  │  └──┐ \n'
            ' │  └─────┘  ┌──┘ \n'
            ' └───────────┘  · '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_1(self):
        grid = Grid([
            [B6, __, __, W5, __, __],
            [__, __, B6, __, __, __],
            [__, __, __, __, __, __],
            [__, __, __, __, __, B4],
            [__, B2, __, __, __, __],
            [__, W2, __, B5, __, __],
        ])
        game_solver = ShingokiSolver(grid)
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
            [__, __, __, W3, __, __],
            [__, __, __, __, __, B2],
            [__, __, __, B3, B2, __],
            [B4, __, __, __, __, __],
            [__, B2, __, __, __, __],
            [__, W2, __, B4, __, B3],
        ])
        game_solver = ShingokiSolver(grid)
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
            [__, __, __, __, __, W6, __, __],
            [__, W3, __, __, __, B6, B4, __],
            [__, __, __, __, __, __, __, __],
            [__, __, B4, __, __, __, __, __],
            [__, __, W2, __, __, __, __, __],
            [__, B2, __, __, __, __, B3, __],
            [B4, B2, __, __, __, B3, __, __],
            [__, __, B3, __, __, B3, __, __]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ·  ┌─────────────────┐ \n'
            ' ·  │  ┌────────┐  ┌──┘ \n'
            ' ·  │  │  ·  ·  │  │  · \n'
            ' ┌──┘  └─────┐  │  │  · \n'
            ' │  ┌─────┐  │  └──┘  · \n'
            ' │  └──┐  │  └─────┐  · \n'
            ' └──┐  │  └─────┐  └──┐ \n'
            ' ·  └──┘  ·  ·  └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_1(self):
        grid = Grid([
            [__, __, __, __, __, B5, __, __],
            [__, __, __, __, __, __, __, __],
            [__, B4, __, __, __, __, __, W3],
            [__, __, __, __, __, __, __, __],
            [__, __, __, __, __, __, __, __],
            [__, B4, __, W4, W6, B4, __, __],
            [W6, B2, __, __, __, __, __, W3],
            [__, __, __, __, __, __, __, B4]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ·  ┌───────────┐  ┌──┐ \n'
            ' ┌──┘  ┌─────┐  └──┘  │ \n'
            ' │  ┌──┘  ·  │  ┌──┐  │ \n'
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
            [B3, __, __, B2, __, __, B2, __, __, W2, __],
            [__, __, __, B3, __, __, B3, __, __, __, __],
            [__, __, __, __, __, W2, __, __, __, __, __],
            [__, B2, __, __, __, __, W3, __, __, __, __],
            [B6, __, __, __, W2, __, __, __, W2, __, __],
            [__, __, __, __, B2, B2, __, __, __, B4, __],
            [__, W2, __, __, __, __, B4, __, __, __, W5],
            [__, __, __, __, __, __, __, B2, B2, __, __],
            [__, __, __, __, W2, __, __, __, B2, __, __],
            [__, B2, __, __, __, __, __, W2, __, __, B2],
            [__, __, __, W4, __, B5, __, __, __, B5, __]
        ])
        game_solver = ShingokiSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  ·  ┌──┐  ·  ┌──┐  ┌─────┐ \n'
            ' │  └─────┘  └─────┘  │  │  ┌──┘ \n'
            ' └──┐  ┌──┐  ┌─────┐  │  │  └──┐ \n'
            ' ·  └──┘  │  └──┐  │  │  └──┐  │ \n'
            ' ┌─────┐  └─────┘  │  └─────┘  │ \n'
            ' │  ┌──┘  ·  ┌──┐  └────────┐  │ \n'
            ' │  │  ·  ┌──┘  └──┐  ·  ┌──┘  │ \n'
            ' │  └──┐  └─────┐  │  ┌──┘  ┌──┘ \n'
            ' └──┐  │  ┌─────┘  │  └──┐  └──┐ \n'
            ' ┌──┘  └──┘  ┌──┐  └─────┘  ┌──┘ \n'
            ' └───────────┘  └───────────┘  · '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)



    # @unittest.skip('This test is too slow (around 10 seconds)')

    # @unittest.skip('This test is too slow (around 21 seconds)')



if __name__ == '__main__':
    unittest.main()
