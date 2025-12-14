from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Miti.MitiSolver import MitiSolver
from Domain.Puzzles.utils import positions


class MitiSolverTest(TestCase):
    def test_6x6_37401(self):
        """https://gridpuzzle.com/miti/37401"""
        size = 6
        dots_positions = positions([(0.5, 2.5), (1.5, -0.5), (1.5, 5.5), (2.5, 3.5), (3.5, 5.5), (4.5, 3.5)])

        expected_solution_str = (
            ' ┌──────────────┐ \n'
            ' └─────┐  ┌─────┘ \n'
            ' ┌──┐  │  └─────┐ \n'
            ' │  │  └──┐  ┌──┘ \n'
            ' │  └─────┘  └──┐ \n'
            ' └──────────────┘ '
        )

        game_solver = MitiSolver(dots_positions, size)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_8x8_31v5k(self):
        """https://gridpuzzle.com/miti/31v5k"""
        size = 8
        dots_positions = positions([(2.5, 7.5), (3.5, 5.5), (4.5, 0.5), (4.5, 3.5), (4.5, 7.5), (5.5, 5.5), (7.5, 5.5)])

        expected_solution_str = (
            ' ┌────────────────────┐ \n'
            ' │  ┌──────────────┐  │ \n'
            ' │  │  ┌────────┐  └──┘ \n'
            ' │  │  └─────┐  └─────┐ \n'
            ' │  └─────┐  └──┐  ┌──┘ \n'
            ' │  ┌─────┘  ┌──┘  └──┐ \n'
            ' │  └────────┘  ┌──┐  │ \n'
            ' └──────────────┘  └──┘ '
        )

        game_solver = MitiSolver(dots_positions, size)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_10x10_210qd(self):
        """https://gridpuzzle.com/miti/210qd"""
        size = 10
        dots_positions = positions([
            (0.5, 7.5), (1.5, 3.5), (1.5, 5.5), (1.5, 9.5), (2.5, 7.5), (4.5, 7.5), (4.5, 9.5), (5.5, 7.5), (6.5, 1.5), (6.5, 5.5), (6.5, 9.5), (7.5, 7.5),
            (9.5, 3.5), (9.5, 7.5)
        ])

        expected_solution_str = (
            ' ┌──────────────────────────┐ \n'
            ' │  ┌─────────────────┐  ┌──┘ \n'
            ' │  │  ┌──┐  ┌──┐  ┌──┘  └──┐ \n'
            ' │  │  │  │  │  └──┘  ┌──┐  │ \n'
            ' │  │  │  │  └────────┘  └──┘ \n'
            ' │  │  │  └─────────────────┐ \n'
            ' │  │  └──────────────┐  ┌──┘ \n'
            ' │  │  ┌────────┐  ┌──┘  └──┐ \n'
            ' │  └──┘  ┌──┐  └──┘  ┌──┐  │ \n'
            ' └────────┘  └────────┘  └──┘ '
        )

        game_solver = MitiSolver(dots_positions, size)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_12x12_0xvnw(self):
        """https://gridpuzzle.com/miti/0xvnw"""
        size = 12
        dots_positions = positions([
            (-0.5, 2.5), (-0.5, 4.5), (-0.5, 8.5), (1.5, 7.5), (1.5, 8.5), (3.5, 2.5), (3.5, 4.5), (3.5, 7.5), (4.5, -0.5), (4.5, 2.5), (4.5, 5.5), (5.5, 5.5),
            (5.5, 7.5), (6.5, 1.5), (6.5, 2.5), (6.5, 9.5), (6.5, 11.5), (7.5, -0.5), (7.5, 6.5), (8.5, 1.5), (8.5, 4.5), (9.5, -0.5), (9.5, 6.5), (9.5, 8.5),
            (9.5, 10.5), (11.5, 3.5), (11.5, 6.5), (11.5, 9.5)
        ])

        expected_solution_str = (
            ' ┌─────┐  ┌──┐  ┌────────┐  ┌─────┐ \n'
            ' │  ┌──┘  │  │  │  ┌─────┘  └──┐  │ \n'
            ' │  │  ┌──┘  │  │  └──┐  ┌──┐  │  │ \n'
            ' │  └──┘  ┌──┘  └──┐  └──┘  │  │  │ \n'
            ' └─────┐  └─────┐  └──┐  ┌──┘  │  │ \n'
            ' ┌──┐  │  ┌─────┘  ┌──┘  └─────┘  │ \n'
            ' │  └──┘  └─────┐  │  ┌───────────┘ \n'
            ' └──┐  ┌─────┐  │  │  └─────┐  ┌──┐ \n'
            ' ┌──┘  └──┐  │  └──┘  ┌──┐  │  │  │ \n'
            ' └─────┐  │  │  ┌─────┘  │  └──┘  │ \n'
            ' ┌─────┘  │  │  └──┐  ┌──┘  ┌──┐  │ \n'
            ' └────────┘  └─────┘  └─────┘  └──┘ '
        )

        game_solver = MitiSolver(dots_positions, size)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)







