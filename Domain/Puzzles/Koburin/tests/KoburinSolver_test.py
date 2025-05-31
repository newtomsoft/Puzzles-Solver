from unittest import TestCase

from Domain.Board.Grid import Grid
from Puzzles.Koburin.KoburinSolver import KoburinSolver

_ = -1


class KoburinSolverTests(TestCase):
    def test_solution_3x3_digit_0(self):
        grid = Grid([
            [_, _, _],
            [_, 0, _],
            [_, _, _],
        ])

        game_solver = KoburinSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐ \n'
            ' │  0  │ \n'
            ' └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x3_digit_1(self):
        grid = Grid([
            [_, 1, _, _],
            [_, _, _, _],
            [_, _, _, _],
        ])
        game_solver = KoburinSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ■  1  ┌──┐ \n'
            ' ┌─────┘  │ \n'
            ' └────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5(self):
        grid = Grid([
            [_, _, 0, _, _],
            [_, _, _, _, _],
            [_, 1, _, 1, _],
            [_, _, _, _, _],
            [_, _, _, _, 0],
        ])

        game_solver = KoburinSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  0  ┌──┐ \n'
            ' │  └─────┘  │ \n'
            ' │  1  ■  1  │ \n'
            ' │  ┌──┐  ┌──┘ \n'
            ' └──┘  └──┘  0 '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8(self):
        grid = Grid([
            [_, _, 0, _, _, 1, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, 3, _, _, _, _, _],
            [_, _, _, _, _, 0, _, _],
            [0, _, _, _, _, _, _, 0],
            [_, _, _, 1, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [0, _, _, _, _, 0, _, _],
        ])

        game_solver = KoburinSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  0  ┌──┐  1  ┌──┐ \n'
            ' │  └─────┘  │  ■  │  │ \n'
            ' │  ■  3  ■  └─────┘  │ \n'
            ' └──┐  ■  ┌──┐  0  ┌──┘ \n'
            ' 0  │  ┌──┘  └──┐  │  0 \n'
            ' ┌──┘  │  1  ■  │  └──┐ \n'
            ' └──┐  └─────┐  └──┐  │ \n'
            ' 0  └────────┘  0  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10(self):
        grid = Grid([
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [0, _, 1, _, 0, _, _, _, _, 0],
            [_, _, _, _, _, 0, _, 0, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [1, _, 1, _, _, _, _, _, _, _],
            [_, _, _, 0, _, _, 2, _, _, _],
            [_, _, _, _, _, 0, _, _, _, _],
            [_, _, _, 2, _, _, _, _, 0, _],
            [0, _, _, _, _, _, _, _, _, _],
        ])

        game_solver = KoburinSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐  ■  ┌──────────────┐ \n'
            ' └──┐  └──┐  └──┐  ■  ┌─────┘ \n'
            ' 0  │  1  │  0  └──┐  └──┐  0 \n'
            ' ┌──┘  ■  └──┐  0  │  0  └──┐ \n'
            ' └────────┐  └─────┘  ┌─────┘ \n'
            ' 1  ■  1  └─────┐  ■  └─────┐ \n'
            ' ┌─────┐  0  ┌──┘  2  ■  ┌──┘ \n'
            ' │  ■  └─────┘  0  ┌──┐  └──┐ \n'
            ' └──┐  ■  2  ■  ┌──┘  │  0  │ \n'
            ' 0  └───────────┘  ■  └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12(self):
        grid = Grid([
            [_, _, _, _, _, 0, _, _, _, _, _, _],
            [_, _, 0, _, _, _, _, 0, _, _, _, _],
            [_, _, _, _, 0, _, _, _, _, _, _, _],
            [_, _, 1, _, _, _, _, 0, _, 0, _, _],
            [_, _, _, _, 1, _, _, _, _, _, _, 0],
            [_, _, _, _, _, _, _, _, 1, _, _, _],
            [_, 2, _, 1, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, 0, _, _, 0, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [0, _, _, _, _, _, 1, _, 1, _, 2, _],
            [_, _, 0, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, 0, _, _, 1, _, _, _]
        ])

        game_solver = KoburinSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ■  ┌────────┐  0  ┌─────┐  ■  ┌──┐ \n'
            ' ┌──┘  0  ┌──┘  ┌──┘  0  └──┐  │  │ \n'
            ' │  ┌─────┘  0  │  ┌─────┐  └──┘  │ \n'
            ' │  │  1  ┌─────┘  │  0  │  0  ┌──┘ \n'
            ' │  │  ■  │  1  ■  └──┐  └─────┘  0 \n'
            ' │  └─────┘  ┌────────┘  1  ■  ┌──┐ \n'
            ' │  2  ■  1  └─────┐  ┌─────┐  │  │ \n'
            ' │  ■  ┌─────┐  0  └──┘  0  └──┘  │ \n'
            ' └──┐  │  ■  └──┐  ■  ┌─────┐  ■  │ \n'
            ' 0  │  └──┐  ■  │  1  │  1  │  2  │ \n'
            ' ┌──┘  0  └──┐  └──┐  │  ■  │  ■  │ \n'
            ' └───────────┘  0  └──┘  1  └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12_evil_j7g24(self):
        # https://gridpuzzle.com/koburin/j7g24
        grid = Grid([
            [_, _, _, 0, _, _, _, _, _, 0, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, 1, _, _, _, _, _, 0, _, _, 0, _],
            [_, _, _, 0, _, _, _, _, 1, _, _, _],
            [_, 1, _, _, 0, _, _, _, _, 1, _, _],
            [_, _, _, _, _, _, 2, _, _, _, _, _],
            [0, _, 2, _, _, _, _, _, _, _, 1, _],
            [_, _, _, _, _, _, 0, _, 0, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, 2, _, _, _, _, 0, _, 0],
            [_, _, 0, _, _, _, 0, _, _, _, _, _],
            [0, _, _, _, _, _, _, _, _, _, _, _]
        ])

        game_solver = KoburinSolver(grid)
        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ■  ┌──┐  0  ┌──┐  ■  ┌──┐  0  ┌──┐ \n'
            ' ┌──┘  └─────┘  │  ┌──┘  │  ┌──┘  │ \n'
            ' │  1  ┌─────┐  └──┘  0  └──┘  0  │ \n'
            ' │  ■  │  0  └──┐  ┌──┐  1  ■  ┌──┘ \n'
            ' │  1  └──┐  0  └──┘  └──┐  1  └──┐ \n'
            ' └──┐  ■  └──┐  ■  2  ■  │  ┌─────┘ \n'
            ' 0  │  2  ┌──┘  ┌─────┐  └──┘  1  ■ \n'
            ' ┌──┘  ■  │  ■  │  0  │  0  ┌─────┐ \n'
            ' └─────┐  └─────┘  ┌──┘  ┌──┘  ┌──┘ \n'
            ' ┌─────┘  ■  2  ■  └─────┘  0  │  0 \n'
            ' └──┐  0  ┌─────┐  0  ┌─────┐  └──┐ \n'
            ' 0  └─────┘  ■  └─────┘  ■  └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12_evil_6r695(self):
        # https://gridpuzzle.com/koburin/6r695
        grid = Grid([
            [0, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, 0, _, _, _, _],
            [_, _, 3, _, _, 0, _, _, 0, _, _, 0],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, 1, _, _, _, _, _, _, _, _, 0, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, 1, _, 0, _, 1, _, _, 0, _, _],
            [_, _, _, _, _, _, _, 1, _, _, _, _],
            [_, _, _, _, _, 1, _, _, _, 0, _, _],
            [_, _, _, _, _, _, _, _, _, _, 1, _],
            [_, 1, _, _, 1, _, _, 2, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
        ])

        game_solver = KoburinSolver(grid)
        expected_0 = (
            ' 0  ┌─────┐  ■  ┌────────┐  ┌─────┐ \n'
            ' ┌──┘  ■  └──┐  └──┐  0  └──┘  ┌──┘ \n'
            ' └──┐  3  ■  │  0  └──┐  0  ┌──┘  0 \n'
            ' ┌──┘  ■  ┌──┘  ┌──┐  └──┐  └─────┐ \n'
            ' │  1  ┌──┘  ┌──┘  │  ■  └──┐  0  │ \n'
            ' │  ■  └──┐  └──┐  └──┐  ┌──┘  ┌──┘ \n'
            ' └──┐  1  │  0  │  1  └──┘  0  └──┐ \n'
            ' ■  │  ■  └─────┘  ■  1  ┌─────┐  │ \n'
            ' ┌──┘  ┌──┐  ■  1  ┌─────┘  0  └──┘ \n'
            ' │  ■  │  └─────┐  └────────┐  1  ■ \n'
            ' │  1  └──┐  1  │  ■  2  ■  └─────┐ \n'
            ' └────────┘  ■  └─────────────────┘ '
        )
        expected_1 = (
            ' 0  ┌─────┐  ■  ┌────────┐  ┌─────┐ \n'
            ' ┌──┘  ■  └──┐  └──┐  0  └──┘  ┌──┘ \n'
            ' │  ■  3  ■  │  0  └──┐  0  ┌──┘  0 \n'
            ' └─────┐  ┌──┘  ┌──┐  └──┐  └─────┐ \n'
            ' ■  1  │  │  ┌──┘  │  ■  └──┐  0  │ \n'
            ' ┌─────┘  │  └──┐  └──┐  ┌──┘  ┌──┘ \n'
            ' └──┐  1  │  0  │  1  └──┘  0  └──┐ \n'
            ' ■  │  ■  └─────┘  ■  1  ┌─────┐  │ \n'
            ' ┌──┘  ┌──┐  ■  1  ┌─────┘  0  └──┘ \n'
            ' │  ■  │  └─────┐  └────────┐  1  ■ \n'
            ' │  1  └──┐  1  │  ■  2  ■  └─────┐ \n'
            ' └────────┘  ■  └─────────────────┘ '
        )
        expected_2 = (
            ' 0  ┌─────┐  ■  ┌────────┐  ┌─────┐ \n'
            ' ┌──┘  ■  └──┐  └──┐  0  └──┘  ┌──┘ \n'
            ' │  ■  3  ■  │  0  └──┐  0  ┌──┘  0 \n'
            ' └────────┐  │  ┌──┐  └──┐  └─────┐ \n'
            ' ■  1  ┌──┘  │  │  │  ■  └──┐  0  │ \n'
            ' ┌─────┘  ┌──┘  │  └──┐  ┌──┘  ┌──┘ \n'
            ' └──┐  1  │  0  │  1  └──┘  0  └──┐ \n'
            ' ■  │  ■  └─────┘  ■  1  ┌─────┐  │ \n'
            ' ┌──┘  ┌──┐  ■  1  ┌─────┘  0  └──┘ \n'
            ' │  ■  │  └─────┐  └────────┐  1  ■ \n'
            ' │  1  └──┐  1  │  ■  2  ■  └─────┐ \n'
            ' └────────┘  ■  └─────────────────┘ '
        )
        expected_3 = (
           ' 0  ┌─────┐  ■  ┌────────┐  ┌─────┐ \n'
           ' ┌──┘  ■  └──┐  └──┐  0  └──┘  ┌──┘ \n'
           ' │  ■  3  ■  │  0  └──┐  0  ┌──┘  0 \n'
           ' └─────┐  ┌──┘  ┌──┐  └──┐  └─────┐ \n'
           ' ■  1  │  └──┐  │  │  ■  └──┐  0  │ \n'
           ' ┌─────┘  ┌──┘  │  └──┐  ┌──┘  ┌──┘ \n'
           ' └──┐  1  │  0  │  1  └──┘  0  └──┐ \n'
           ' ■  │  ■  └─────┘  ■  1  ┌─────┐  │ \n'
           ' ┌──┘  ┌──┐  ■  1  ┌─────┘  0  └──┘ \n'
           ' │  ■  │  └─────┐  └────────┐  1  ■ \n'
           ' │  1  └──┐  1  │  ■  2  ■  └─────┐ \n'
           ' └────────┘  ■  └─────────────────┘ '
        )
        expected_4 = (
           ' 0  ┌─────┐  ■  ┌────────┐  ┌─────┐ \n'
           ' ┌──┘  ■  └──┐  └──┐  0  └──┘  ┌──┘ \n'
           ' │  ■  3  ■  │  0  └──┐  0  ┌──┘  0 \n'
           ' └────────┐  └──┐  ■  └──┐  └─────┐ \n'
           ' ■  1  ┌──┘  ┌──┘  ┌──┐  └──┐  0  │ \n'
           ' ┌─────┘  ┌──┘  ┌──┘  │  ┌──┘  ┌──┘ \n'
           ' └──┐  1  │  0  │  1  └──┘  0  └──┐ \n'
           ' ■  │  ■  └─────┘  ■  1  ┌─────┐  │ \n'
           ' ┌──┘  ┌──┐  ■  1  ┌─────┘  0  └──┘ \n'
           ' │  ■  │  └─────┐  └────────┐  1  ■ \n'
           ' │  1  └──┐  1  │  ■  2  ■  └─────┐ \n'
           ' └────────┘  ■  └─────────────────┘ '
        )
        expected_5 = (
           ' 0  ┌─────┐  ■  ┌────────┐  ┌─────┐ \n'
           ' ┌──┘  ■  └──┐  └──┐  0  └──┘  ┌──┘ \n'
           ' │  ■  3  ■  │  0  └──┐  0  ┌──┘  0 \n'
           ' └────────┐  └─────┐  └──┐  └─────┐ \n'
           ' ■  1  ┌──┘  ┌─────┘  ■  └──┐  0  │ \n'
           ' ┌─────┘  ┌──┘  ┌─────┐  ┌──┘  ┌──┘ \n'
           ' └──┐  1  │  0  │  1  └──┘  0  └──┐ \n'
           ' ■  │  ■  └─────┘  ■  1  ┌─────┐  │ \n'
           ' ┌──┘  ┌──┐  ■  1  ┌─────┘  0  └──┘ \n'
           ' │  ■  │  └─────┐  └────────┐  1  ■ \n'
           ' │  1  └──┐  1  │  ■  2  ■  └─────┐ \n'
           ' └────────┘  ■  └─────────────────┘ '
        )
        expected_solutions = {expected_0, expected_1, expected_2, expected_3, expected_4, expected_5}
        solution_0 = game_solver.get_solution()
        solution_1 = game_solver.get_other_solution()
        solution_2 = game_solver.get_other_solution()
        solution_3 = game_solver.get_other_solution()
        solution_4 = game_solver.get_other_solution()
        solution_5 = game_solver.get_other_solution()
        solution_6 = game_solver.get_other_solution()
        str_solutions = {str(solution_0), str(solution_1), str(solution_2), str(solution_3), str(solution_4), str(solution_5)}
        self.assertEqual(expected_solutions, str_solutions)
        self.assertEqual(Grid.empty(), solution_6)
