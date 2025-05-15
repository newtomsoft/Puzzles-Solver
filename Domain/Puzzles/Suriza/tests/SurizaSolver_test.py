import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Suriza.SurizaSolver import SurizaSolver

_ = ' '


class SurizaSolverTests(TestCase):


    def test_solution_with_013_0(self):
        grid = Grid([
            [1, _],
            [3, _],
            [_, 3],
            [0, _],
        ])
        game_solver = SurizaSolver(grid)

        solution = game_solver.get_solution()
        expected_solution_string = (
            '         \n'
            ' ┌─────┐ \n'
            ' └──┐  │ \n'
            '    └──┘ \n'
            '         '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_with_013_1(self):
        grid = Grid([
            [0, _],
            [_, 3],
            [3, _],
            [1, _],
        ])
        game_solver = SurizaSolver(grid)

        solution = game_solver.get_solution()
        expected_solution_string = (
            '         \n'
            '    ┌──┐ \n'
            ' ┌──┘  │ \n'
            ' └─────┘ \n'
            '         '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_with_2(self):
        grid = Grid([
            [2, 2],
            [2, 2]
        ])
        game_solver = SurizaSolver(grid)

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' │     │ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6(self):
        grid = Grid([
            [_, _, _, _, 2],
            [_, _, _, 2, _],
            [_, _, 3, 2, _],
            [_, _, 0, _, _],
            [_, 3, 3, _, 3]
        ])
        game_solver = SurizaSolver(grid)

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──────────────┐ \n'
            ' │  ┌────────┐  │ \n'
            ' │  │  ┌──┐  └──┘ \n'
            ' │  └──┘  └─────┐ \n'
            ' │  ┌──┐  ┌──┐  │ \n'
            ' └──┘  └──┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8(self):
        grid = Grid([
            [_, _, 3, _, _, 2, _],
            [2, 1, 3, _, 3, _, 3],
            [2, 2, _, 2, _, _, 3],
            [_, _, _, _, _, _, 3],
            [_, _, _, 2, 3, _, _],
            [2, _, 2, 1, 2, 2, _],
            [_, 3, 3, _, 3, 2, 3]
        ])
        game_solver = SurizaSolver(grid)

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌────────┐     ┌─────┐ \n'
            ' │     ┌──┘  ┌──┘  ┌──┘ \n'
            ' └──┐  └──┐  └──┐  └──┐ \n'
            '    └──┐  └─────┘  ┌──┘ \n'
            ' ┌──┐  └──┐  ┌──┐  └──┐ \n'
            ' │  └─────┘  │  └──┐  │ \n'
            ' └──┐  ┌──┐  └──┐  │  │ \n'
            '    └──┘  └─────┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_11x11(self):
        grid = Grid([
            [_, 2, 3, _, _, 1, _, 1, _, 3],
            [_, 3, _, 2, _, 3, _, _, 3, _],
            [2, 1, 1, _, _, _, _, 2, _, _],
            [_, 2, _, _, _, _, _, _, 1, 3],
            [_, 1, _, 3, _, 3, 0, _, _, 3],
            [3, _, _, _, _, _, _, 2, _, _],
            [_, 1, _, _, 1, 3, _, _, 3, _],
            [_, 3, _, _, 2, 2, _, _, _, 3],
            [1, _, _, _, _, _, _, _, 3, 2],
            [_, _, _, _, _, _, _, 2, _, _]
        ])
        game_solver = SurizaSolver(grid)

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  ┌──┐  ┌─────────────────┐ \n'
            ' │  │  │  │  └──┐  ┌──┐  ┌─────┘ \n'
            ' │  └──┘  └──┐  └──┘  │  └──┐    \n'
            ' └──┐  ┌──┐  └─────┐  └──┐  └──┐ \n'
            ' ┌──┘  │  └──┐  ┌──┘     │  ┌──┘ \n'
            ' └──┐  │  ┌──┘  └──┐  ┌──┘  └──┐ \n'
            ' ┌──┘  │  │     ┌──┘  │  ┌─────┘ \n'
            ' └──┐  │  └──┐  └──┐  │  └─────┐ \n'
            '    └──┘     └──┐  └──┘  ┌─────┘ \n'
            ' ┌──────────────┘  ┌──┐  └─────┐ \n'
            ' └─────────────────┘  └────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_16x16(self):
        grid = Grid([
            [_, _, 2, 3, _, 2, _, _, _, _, _, _, _, _, _],
            [_, _, 2, _, 2, 2, 3, 3, 3, 2, _, _, 3, _, _],
            [_, _, 2, _, 3, _, _, _, _, 1, _, _, 2, 2, 2],
            [3, _, 3, 2, _, 0, 2, _, _, 3, 2, 2, _, 1, _],
            [_, 2, _, _, _, 3, _, _, 2, _, _, 1, 3, 2, _],
            [_, _, 2, _, _, 2, _, 1, _, _, _, _, 2, _, _],
            [_, _, _, _, 2, _, 3, _, 3, 1, 2, _, _, _, 1],
            [2, 1, _, 2, _, 1, _, _, 2, 3, 1, _, 1, 3, _],
            [3, 1, _, 1, 2, 2, 3, _, _, _, _, _, 3, _, _],
            [_, _, _, _, 2, 3, 2, 1, _, _, _, _, _, 2, 2],
            [_, _, 2, 3, _, _, 2, 2, _, 2, _, 2, _, 2, 1],
            [3, _, _, _, _, 2, _, 1, _, _, 2, 3, _, 3, _],
            [3, 0, _, 3, _, 2, _, 3, 3, 3, 2, _, _, _, 1],
            [3, 2, 2, 2, _, _, 3, _, _, _, _, 3, _, _, 2],
            [_, _, _, _, 2, _, _, 3, _, 3, _, 2, 2, _, 3]
        ])
        game_solver = SurizaSolver(grid)

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐  ┌──┐  ┌──────────────┐  ┌───────────┐ \n'
            ' │  ┌──┘  │  │  │  ┌──┐  ┌──┐  │  │  ┌─────┐  │ \n'
            ' │  └─────┘  │  │  │  └──┘  │  └──┘  └──┐  └──┘ \n'
            ' └──┐  ┌──┐  └──┘  └─────┐  │  ┌─────┐  └─────┐ \n'
            ' ┌──┘  │  └─────┐  ┌──┐  │  └──┘     └──┐  ┌──┘ \n'
            ' │  ┌──┘  ┌──┐  └──┘  │  └──┐  ┌────────┘  └──┐ \n'
            ' │  │  ┌──┘  └─────┐  │  ┌──┘  └──┐  ┌────────┘ \n'
            ' └──┘  └──┐  ┌──┐  └──┘  └─────┐  └──┘  ┌──┐    \n'
            ' ┌────────┘  │  │  ┌──┐  ┌─────┘  ┌──┐  │  └──┐ \n'
            ' └──┐  ┌──┐  │  │  │  │  └─────┐  │  └──┘  ┌──┘ \n'
            ' ┌──┘  │  │  │  └──┘  │  ┌─────┘  └──┐  ┌──┘    \n'
            ' └──┐  │  └──┘     ┌──┘  └────────┐  │  │  ┌──┐ \n'
            ' ┌──┘  └─────┐  ┌──┘  ┌──┐  ┌──┐  └──┘  └──┘  │ \n'
            ' └──┐  ┌─────┘  │  ┌──┘  └──┘  └─────┐  ┌──┐  │ \n'
            ' ┌──┘  │  ┌─────┘  └─────┐  ┌────────┘  │  │  │ \n'
            ' └─────┘  └──────────────┘  └───────────┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
