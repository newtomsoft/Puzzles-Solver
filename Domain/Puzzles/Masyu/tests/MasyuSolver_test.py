import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Masyu.MasyuSolver import MasyuSolver

_ = ' '
W = 'w'
B = 'b'

class MasyuSolverTests(TestCase):
    def test_solution_white_0(self):
        grid = Grid([
            [_, W, _],
            [_, W, _],
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
            [_, W, _],
            [_, _, _],
            [_, W, _],
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
            [_, W, _, _],
            [W, _, _, W],
            [_, _, W, _],
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
            [B, _, _],
            [_, _, _],
            [_, _, B],
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
            [B, _, W, _],
            [_, _, W, _],
            [_, _, _, _]
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
            [B, W, _, _, _, _],
            [W, _, _, W, W, _],
            [_, B, W, _, _, _],
            [_, W, _, _, _, B],
            [W, _, _, W, _, _],
            [B, _, _, W, _, _]
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
            [_, B, _, _, W, _],
            [_, _, _, _, _, _],
            [_, W, B, W, _, B],
            [_, _, _, _, _, B],
            [_, _, _, _, _, _],
            [B, _, _, _, W, _]
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
            [B, W, _, W, _, _, W, _],
            [W, _, _, _, _, _, _, W],
            [_, _, _, _, W, _, _, _],
            [_, W, W, _, _, _, _, _],
            [_, _, _, B, W, W, _, W],
            [_, _, W, _, _, _, _, _],
            [B, W, _, _, W, W, _, _],
            [_, _, _, _, W, _, W, B]
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
            [_, _, _, _, _, _, _, B],
            [W, _, B, _, B, _, _, _],
            [W, _, _, _, _, W, _, _],
            [_, W, _, _, _, _, W, _],
            [_, _, _, _, _, _, _, _],
            [B, _, _, B, B, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, W, _, W, _, _, _, B]
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
            [_, _, B, W, _, _, _, _, _, B],
            [W, _, W, _, B, W, _, W, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, W, _, B, _, _, W, _, _],
            [_, W, B, W, _, _, _, W, _, _],
            [W, B, W, _, _, W, W, B, _, B],
            [_, _, _, _, _, _, _, _, B, _],
            [_, _, W, _, _, _, _, _, _, _],
            [W, _, _, _, B, W, W, _, _, _],
            [B, W, B, B, _, _, _, _, W, _]
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
            [_, _, B, W, _, _, B, B, _, _],
            [_, _, W, _, _, _, W, W, _, W],
            [W, _, _, _, W, _, W, W, _, W],
            [_, W, W, _, W, W, _, _, _, _],
            [W, _, _, _, _, _, _, _, W, _],
            [_, _, B, W, B, _, _, _, W, _],
            [_, _, W, _, _, _, _, W, _, _],
            [_, W, W, _, _, W, _, _, _, W],
            [_, _, _, W, W, _, W, _, _, W],
            [_, _, _, B, _, W, _, _, W, B]
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
            [_, _, _, _, W, _, _, _, _, _],
            [_, _, _, _, _, _, _, W, _, _],
            [W, B, _, B, _, B, _, _, _, _],
            [_, _, _, _, _, _, B, W, _, _],
            [_, _, _, W, _, B, _, _, _, W],
            [_, B, _, B, _, W, _, _, _, _],
            [_, _, _, _, _, _, _, W, _, _],
            [_, _, _, _, W, _, _, _, _, _],
            [_, _, _, W, _, W, _, W, _, _],
            [_, _, B, _, _, _, W, _, W, _]
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
            [_, _, _, _, W, _, _, W, _, _, _, _, W, B, _],
            [_, W, _, W, _, _, _, _, W, W, B, _, _, W, _],
            [_, B, _, _, _, W, W, _, _, _, _, B, _, _, _],
            [_, _, B, W, _, _, W, _, _, _, B, _, B, _, B],
            [_, W, _, _, _, _, _, _, _, _, _, _, _, _, W],
            [_, W, _, _, _, W, _, _, W, W, _, W, _, _, _],
            [_, B, W, _, _, _, _, _, _, W, _, _, _, _, _],
            [_, W, W, _, W, W, W, _, _, _, _, _, W, B, W],
            [W, _, _, _, _, _, _, _, _, W, W, _, _, _, _],
            [_, _, _, W, W, _, _, B, _, B, _, W, _, _, W],
            [_, _, _, W, _, B, _, B, W, W, B, W, _, W, _],
            [B, W, _, W, B, W, W, _, _, _, _, _, _, W, _],
            [B, _, _, _, _, _, _, _, _, W, W, _, _, _, _],
            [W, _, _, W, _, _, W, W, _, W, _, _, W, W, W],
            [_, _, _, _, W, _, _, _, _, _, B, W, B, _, _]
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


if __name__ == '__main__':
    unittest.main()
