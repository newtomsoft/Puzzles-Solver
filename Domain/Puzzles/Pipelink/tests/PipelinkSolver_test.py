import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Puzzles.Pipelink.PipelinkSolver import PipelinkSolver


class PipelinkSolverTests(TestCase):
    def test_solution_basic_4x4(self):
        grid_str = (
            ' ·  ·  ·  · \n'
            ' · ─┼──┘  · \n'
            ' · ─┼─ ·  · \n'
            ' ·  ·  ·  · '
        )
        game_solver = PipelinkSolver(Grid.from_str(grid_str, type(Island)))

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  ┌──┐ \n'
            ' └──┼──┘  │ \n'
            ' ┌──┼──┐  │ \n'
            ' └──┘  └──┘ '
        )

        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_basic_4x4_2_solutions(self):
        grid_str = (
            ' ·  ·  ·  · \n'
            ' · ─┼─ ·  · \n'
            ' · ─┼─ ·  · \n'
            ' ·  ·  ·  · '
        )
        game_solver = PipelinkSolver(Grid.from_str(grid_str, type(Island)))

        first_solution = game_solver.get_solution()
        second_solution = game_solver.get_other_solution()

        expected_first_solution_string = (
            ' ┌──┐  ┌──┐ \n'
            ' └──┼──┘  │ \n'
            ' ┌──┼──┐  │ \n'
            ' └──┘  └──┘ '
        )
        expected_second_solution_string = (
            ' ┌──┐  ┌──┐ \n'
            ' └──┼──┼──┘ \n'
            ' ┌──┼──┼──┐ \n'
            ' └──┘  └──┘ '
        )

        self.assertEqual({expected_first_solution_string, expected_second_solution_string}, {str(first_solution), str(second_solution)})
        third_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), third_solution)


    def test_solution_5x5_easy_3e2vn(self):
        """https://gridpuzzle.com/pipelink/3e2vn"""
        grid_str = (
            ' · ─── ·  ·  · \n'
            ' ·  ·  · ─┐  · \n'
            ' ·  · ─┘  ·  · \n'
            ' ·  │  ·  ·  · \n'
            ' ·  ·  · ─── · '
        )
        game_solver = PipelinkSolver(Grid.from_str(grid_str, type(Island)))

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌───────────┐ \n'
            ' └──┐  ┌──┐  │ \n'
            ' ┌──┼──┘  │  │ \n'
            ' │  │  ┌──┘  │ \n'
            ' └──┘  └─────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_hard_1yv19(self):
        """https://gridpuzzle.com/pipelink/1yv19"""
        grid_str = (
            ' ┌─ ·  ·  ·  ·  · \n'
            ' ·  ·  ·  └─ ·  · \n'
            ' · ─── ·  · ─┼─ · \n'
            ' ·  · ─┘  ·  ·  · \n'
            ' ·  ·  · ─┼─ · ─┐ \n'
            ' · ─── ·  ·  ·  · '

        )
        game_solver = PipelinkSolver(Grid.from_str(grid_str, type(Island)))

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌────────┐  ┌──┐ \n'
            ' └─────┐  └──┼──┘ \n'
            ' ┌─────┼─────┼──┐ \n'
            ' └─────┘  ┌──┼──┘ \n'
            ' ┌────────┼──┼──┐ \n'
            ' └────────┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x7_expert_2ykw8(self):
        """https://gridpuzzle.com/pipelink/2ykw8"""
        grid_str = (
            ' ·  · ─── ·  · ─── · \n'
            ' └─ ·  · ─┘  │  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  · \n'
            ' ·  └─ ·  ·  · ─┐  · \n'
            ' ·  ·  · ─┐  ·  ·  · \n'
            ' ·  · ─┐  ·  ·  │  · \n'
            ' ·  ·  ·  · ─┘  ·  · '
        )
        game_solver = PipelinkSolver(Grid.from_str(grid_str, type(Island)))

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌────────┐  ┌─────┐ \n'
            ' └──┐  ┌──┘  │  ┌──┘ \n'
            ' ┌──┼──┘  ┌──┘  └──┐ \n'
            ' │  └─────┘  ┌──┐  │ \n'
            ' │  ┌─────┐  │  │  │ \n'
            ' │  └──┐  │  │  │  │ \n'
            ' └─────┘  └──┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_evil_09ny2(self):
        """https://gridpuzzle.com/pipelink/09ny2"""
        grid_str = (
            ' ·  ·  ·  ·  ·  ·  ·  · \n'
            ' · ─── ·  · ─┘  · ─┘  · \n'
            ' ·  ·  · ─┘  ·  ·  ·  · \n'
            ' ·  · ─┘  ·  ·  · ─┼─ · \n'
            ' · ─┘  ·  ·  · ─┐  ·  · \n'
            ' ·  ·  ·  · ─┘  ·  ·  · \n'
            ' ·  │  ·  ┌─ ·  · ─── · \n'
            ' ·  ·  ·  ·  ·  ·  ·  · '
        )
        game_solver = PipelinkSolver(Grid.from_str(grid_str, type(Island)))

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌────────┐  ┌──┐  ┌──┐ \n'
            ' └────────┼──┘  └──┘  │ \n'
            ' ┌──┐  ┌──┘  ┌──┐  ┌──┘ \n'
            ' └──┼──┘  ┌──┘  └──┼──┐ \n'
            ' ┌──┘  ┌──┘  ┌──┐  │  │ \n'
            ' │  ┌──┼─────┘  │  └──┘ \n'
            ' │  │  │  ┌──┐  └─────┐ \n'
            ' └──┘  └──┘  └────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_evil_48d1p(self):
        """https://gridpuzzle.com/pipelink/48d1p"""
        grid_str = (
           ' · ─── ·  ·  ·  ·  ·  · ─── · \n'
           ' ·  ·  ·  └─ ·  │  │  ·  ·  │ \n'
           ' ·  ·  │  ·  ·  ·  ·  ·  ·  · \n'
           ' ·  ·  ·  ·  ·  │  ·  ┌─ ·  · \n'
           ' · ─┘  ┌─ ·  ·  · ─┼─ ·  · ─┘ \n'
           ' └─ ·  · ─┘  ·  ·  · ─┐  └─ · \n'
           ' ·  ·  ┌─ · ─┐  ·  ·  ·  ·  · \n'
           ' ·  ·  ·  ·  ·  ·  · ─┐  ·  · \n'
           ' │  ·  · ─┼──┐  ·  │  ·  ·  · \n'
           ' · ─┘  ·  ·  ·  ·  ·  ·  └─ · '
        )
        game_solver = PipelinkSolver(Grid.from_str(grid_str, type(Island)))

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌─────┐  ┌─────┐  ┌────────┐ \n'
            ' └──┐  │  └──┐  │  │  ┌──┐  │ \n'
            ' ┌──┘  │  ┌──┼──┼──┼──┘  └──┘ \n'
            ' └──┐  └──┼──┘  │  │  ┌─────┐ \n'
            ' ┌──┘  ┌──┼──┐  └──┼──┘  ┌──┘ \n'
            ' └──┐  └──┘  └──┐  └──┐  └──┐ \n'
            ' ┌──┘  ┌─────┐  └──┐  └──┐  │ \n'
            ' │  ┌──┘  ┌──┘  ┌──┼──┐  │  │ \n'
            ' │  │  ┌──┼──┐  │  │  │  │  │ \n'
            ' └──┘  └──┘  └──┘  └──┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_evil_de0yv(self):
        """https://gridpuzzle.com/pipelink/de0yv"""
        grid_str = (
           ' ·  ·  ·  ·  ·  ·  ·  ·  ┌─ · \n'
           ' ·  · ─┐  ·  ·  │  ·  ·  ·  · \n'
           ' · ─┐  · ─── ·  ·  · ─┘  ·  · \n'
           ' ·  ·  ·  ·  · ─┐  ·  ·  │  · \n'
           ' ·  ·  └─ ·  ·  · ─── ·  · ─┘ \n'
           ' ┌─ ·  ·  └─ ·  ·  ·  │  ·  · \n'
           ' ·  └─ ·  ·  ┌─ ·  ·  ·  ·  · \n'
           ' ·  ·  └─ ·  ·  · ─┐  ·  ┌─ · \n'
           ' ·  ·  ·  ·  │  ·  ·  └─ ·  · \n'
           ' · ─┘  ·  ·  ·  ·  ·  ·  ·  · '
        )
        game_solver = PipelinkSolver(Grid.from_str(grid_str, type(Island)))

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌────────┐  ┌──┐  ┌──┐  ┌──┐ \n'
            ' └─────┐  └──┘  │  │  │  │  │ \n'
            ' ┌──┐  └─────┐  └──┼──┘  │  │ \n'
            ' │  └──┐  ┌──┼──┐  └──┐  │  │ \n'
            ' └──┐  └──┼──┼──┼─────┼──┼──┘ \n'
            ' ┌──┼──┐  └──┘  └──┐  │  └──┐ \n'
            ' │  └──┼──┐  ┌──┐  └──┼─────┘ \n'
            ' └──┐  └──┼──┼──┼──┐  │  ┌──┐ \n'
            ' ┌──┼──┐  │  │  └──┘  └──┘  │ \n'
            ' └──┘  └──┘  └──────────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12_evil_25k9d(self):
        """https://gridpuzzle.com/pipelink/25k9d"""
        grid_str = (
            ' ·  ·  · ─── ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  · ─┐  · ─┼─ ·  ·  ·  · \n'
            ' │  ·  ┌─ · ─┼─ ·  ·  ·  · ─┐  ·  · \n'
            ' ·  └─ · ─┘  ·  ·  ·  ·  │  ·  · ─┐ \n'
            ' ·  ·  ·  ┌─ ·  ┌─ ·  └─ ·  ·  ┌─ · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  │  ·  ·  · \n'
            ' ·  ·  ┌──┼─ ·  · ─┐  ·  · ─┘  ·  · \n'
            ' · ─┘  ·  ·  · ─┐  ·  └─ ·  ·  ·  │ \n'
            ' ┌─ · ─┐  ┌─ ·  ·  ·  ·  ·  ·  └─ · \n'
            ' ·  ·  ·  ·  ·  ·  · ─┘  · ─── ·  · \n'
            ' ·  · ─┐  · ─┼─ ·  ·  ┌─ ·  ·  ·  · \n'
            ' ·  ·  · ─── ·  ·  ·  ·  ·  ·  ·  · '
        )
        game_solver = PipelinkSolver(Grid.from_str(grid_str, type(Island)))

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  ┌───────────┐  ┌─────┐  ┌──┐ \n'
            ' │  │  └──┐  ┌──┐  └──┼──┐  └──┘  │ \n'
            ' │  │  ┌──┼──┼──┼──┐  └──┼──┐  ┌──┘ \n'
            ' │  └──┼──┘  │  └──┼──┐  │  │  └──┐ \n'
            ' └──┐  │  ┌──┘  ┌──┘  └──┼──┘  ┌──┘ \n'
            ' ┌──┼──┘  │  ┌──┼─────┐  │  ┌──┼──┐ \n'
            ' │  │  ┌──┼──┘  └──┐  │  └──┘  │  │ \n'
            ' └──┘  └──┘  ┌──┐  │  └─────┐  │  │ \n'
            ' ┌─────┐  ┌──┼──┘  └──┐  ┌──┘  └──┘ \n'
            ' └──┐  └──┼──┼──┐  ┌──┘  └────────┐ \n'
            ' ┌──┼──┐  └──┼──┼──┘  ┌──┐  ┌──┐  │ \n'
            ' └──┘  └─────┘  └─────┘  └──┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_12x12_evil_41d1p(self):
        """https://gridpuzzle.com/pipelink/41d1p"""
        grid_str = (
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  · ─┘  ·  └─ ·  · ─┘  · \n'
            ' · ─── ·  └─ ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  · ─── ·  └─ ·  │  · \n'
            ' ·  · ─── ·  │  ┌─ ·  │  ·  ·  ·  │ \n'
            ' ·  · ─── ·  ·  ·  │  ·  ·  ┌─ ·  · \n'
            ' └─ ·  ·  · ─┐  ·  ·  · ─┼─ ·  └─ · \n'
            ' ·  · ─┘  ·  ·  · ─── ·  │  ·  ·  · \n'
            ' · ─── ·  ·  ·  ·  ·  ·  ·  · ─── · \n'
            ' ·  ·  · ─┐  │  ·  ┌─ · ─┐  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  │  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  └─ ·  ·  └─ · '
        )
        game_solver = PipelinkSolver(Grid.from_str(grid_str, type(Island)))

        solution = game_solver.get_solution()
        expected_solution_string = (
            ' ┌──┐  ┌────────┐  ┌──┐  ┌──┐  ┌──┐ \n'
            ' │  └──┘  ┌─────┘  │  └──┘  └──┘  │ \n'
            ' └─────┐  └─────┐  └─────┐  ┌──┐  │ \n'
            ' ┌─────┘  ┌──┐  └─────┐  └──┘  │  │ \n'
            ' │  ┌─────┘  │  ┌──┐  │  ┌─────┘  │ \n'
            ' │  └─────┐  └──┘  │  │  │  ┌──┐  │ \n'
            ' └─────┐  └──┐  ┌──┘  └──┼──┘  └──┘ \n'
            ' ┌─────┘  ┌──┘  └─────┐  │  ┌─────┐ \n'
            ' └─────┐  └──┐  ┌─────┘  └──┼─────┘ \n'
            ' ┌──┐  └──┐  │  │  ┌─────┐  └─────┐ \n'
            ' │  └─────┘  │  │  │  ┌──┘  ┌──┐  │ \n'
            ' └───────────┘  └──┘  └─────┘  └──┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15_evil_029dr(self):
        """https://gridpuzzle.com/pipelink/029dr"""
        grid_str = (
           ' ·  ·  ·  ·  ·  ·  ·  ┌─ ·  ·  ·  ·  ·  ·  · \n'
           ' ·  ·  └─ ·  └─ ·  ·  ·  ·  ·  ·  ·  │  ·  · \n'
           ' │  · ─┐  ·  ·  ·  ┌─ ·  ┌──┼─ ·  │  │  · ─┐ \n'
           ' ·  ·  ·  ·  └─ ·  ·  ·  ·  ·  └─ ·  ·  ·  · \n'
           ' · ─┘  ·  ·  · ─┼──┐  └──┐  ·  ·  ·  ·  └─ · \n'
           ' ·  ·  ·  ┌─ ·  ·  ·  ·  └─ · ─┘  ┌─ ·  ┌─ · \n'
           ' ·  ·  ┌─ ·  · ─── ·  ·  ·  ·  ·  · ─┐  ·  · \n'
           ' · ─── · ─┐  ·  ·  └─ ·  └─ ·  ·  ┌─ ·  ┌─ · \n'
           ' ·  · ─┘  ·  ·  ·  ·  ·  ·  └─ ·  · ─┐  ·  · \n'
           ' ·  └─ ·  └──┼─ ·  └─ ·  ·  ·  · ─┐  ·  ·  · \n'
           ' ·  ┌─ ·  ·  ·  · ─┐  └─────── ·  ·  ·  ┌─ · \n'
           ' ·  ·  ·  · ─┐  ·  ·  ·  ·  ·  └─ ·  ·  ·  · \n'
           ' ┌─ ·  └──── ·  │  ┌─ · ─┘  ·  ·  · ─── ·  │ \n'
           ' ·  · ─┐  ·  ·  ·  ·  ·  ·  ·  │  · ─── ·  · \n'
           ' ·  ·  ·  ·  ·  ·  ·  └─ ·  ·  ·  ·  ·  ·  · '
        )
        game_solver = PipelinkSolver(Grid.from_str(grid_str, type(Island)))

        solution = game_solver.get_solution()
        expected_solution_string = (
           ' ┌──┐  ┌─────┐  ┌──┐  ┌─────┐  ┌──┐  ┌─────┐ \n'
           ' │  │  └──┐  └──┘  └──┼─────┼──┘  │  │  ┌──┘ \n'
           ' │  └──┐  │  ┌──┐  ┌──┘  ┌──┼──┐  │  │  └──┐ \n'
           ' └──┐  └──┘  └──┼──┘  ┌──┘  │  └──┼──┘  ┌──┘ \n'
           ' ┌──┘  ┌────────┼──┐  └──┐  └──┐  └──┐  └──┐ \n'
           ' │  ┌──┘  ┌─────┘  └──┐  └─────┘  ┌──┘  ┌──┘ \n'
           ' └──┘  ┌──┘  ┌─────┐  └──┐  ┌──┐  └──┐  └──┐ \n'
           ' ┌─────┼──┐  └──┐  └──┐  └──┼──┘  ┌──┘  ┌──┘ \n'
           ' │  ┌──┘  │  ┌──┼──┐  └──┐  └──┐  └──┐  └──┐ \n'
           ' │  └──┐  └──┼──┘  └──┐  └─────┼──┐  └─────┘ \n'
           ' │  ┌──┘  ┌──┘  ┌──┐  └────────┼──┼──┐  ┌──┐ \n'
           ' └──┼──┐  └──┐  │  └──┐  ┌──┐  └──┘  └──┘  │ \n'
           ' ┌──┘  └─────┘  │  ┌──┼──┘  │  ┌────────┐  │ \n'
           ' │  ┌──┐  ┌──┐  └──┼──┼─────┘  │  ┌─────┘  │ \n'
           ' └──┘  └──┘  └─────┘  └────────┘  └────────┘ '
        )
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
