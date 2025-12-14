import unittest
from unittest import TestCase

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Puzzles.RoundTrip.RoundTripSolver import RoundTripSolver

_ = RoundTripSolver.empty


class RoundTripSolverTests(TestCase):
    def test_solution_5x5_basic(self):
        grid_str = (
            ' ·  · ─┐  ·  · \n'
            ' ┌──┘  ·  · ─┐ \n'
            ' · ─┐  └──┼─ · \n'
            ' ┌─ ·  · ─┼──┐ \n'
            ' · ─┘  ·  · ─┘ '
        )
        clues = {
            Direction.down(): [2, 2, 3, 4, 2],
            Direction.left(): [2, 2, 3, 5, 2],
            Direction.up(): [2, 3, 3, 4, 2],
            Direction.right(): [2, 2, 2, 5, 2],
        }

        expected_solution_string = (
            ' ·  ┌──┐  ·  · \n'
            ' ┌──┘  │  ┌──┐ \n'
            ' └──┐  └──┼──┘ \n'
            ' ┌──┼─────┼──┐ \n'
            ' └──┘  ·  └──┘ '
        )

        game_solver = RoundTripSolver(Grid.from_str(grid_str, type(Island)), clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_only_clues(self):
        grid_str = (
            ' ·  ·  ·  ·  · \n'
            ' │  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  · '
        )
        clues = {
            Direction.down(): [5, _, _, _, 5],
            Direction.left(): [5, _, _, _, 5],
            Direction.up(): [5, _, _, _, 5],
            Direction.right(): [5, _, _, _, 5],
        }

        expected_solution_string = (
            ' ┌───────────┐ \n'
            ' │  ·  ·  ·  │ \n'
            ' │  ·  ·  ·  │ \n'
            ' │  ·  ·  ·  │ \n'
            ' └───────────┘ '
        )

        game_solver = RoundTripSolver(Grid.from_str(grid_str, type(Island)), clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

        game_solver = RoundTripSolver(Grid.from_str(grid_str, type(Island)), clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_basic_with_clue(self):
        grid_str = (
            ' ·  · ─┐  ·  · \n'
            ' ┌──┘  ·  · ─┐ \n'
            ' · ─┐  └──┼─ · \n'
            ' ┌─ ·  · ─┼──┐ \n'
            ' ·  ·  ·  · ─┘ '
        )
        clues = {
            Direction.down(): [_, _, _, _, _],
            Direction.left(): [_, _, _, _, _],
            Direction.up(): [_, _, _, _, _],
            Direction.right(): [_, _, _, _, 2],
        }

        expected_solution_string = (
            ' ·  ┌──┐  ·  · \n'
            ' ┌──┘  │  ┌──┐ \n'
            ' └──┐  └──┼──┘ \n'
            ' ┌──┼─────┼──┐ \n'
            ' └──┘  ·  └──┘ '
        )

        game_solver = RoundTripSolver(Grid.from_str(grid_str, type(Island)), clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_easy_31yk6(self):
        """https://gridpuzzle.com/round-trip/31yk6"""
        grid_str = (
            ' ·  ·  ·  ·  · \n'
            ' ·  ·  │  ·  · \n'
            ' └─ ·  └─ ·  · \n'
            ' ┌─ ·  ·  · ─┐ \n'
            ' ·  ·  ·  └─ · '
        )
        clues = {
            Direction.down(): [2, 2, 3, 4, 2],
            Direction.left(): [2, 2, 3, 5, 2],
            Direction.up(): [2, 3, 3, 4, 2],
            Direction.right(): [2, 2, 2, 5, 2],
        }

        expected_solution_string = (
            ' ·  ┌──┐  ·  · \n'
            ' ┌──┘  │  ┌──┐ \n'
            ' └──┐  └──┼──┘ \n'
            ' ┌──┼─────┼──┐ \n'
            ' └──┘  ·  └──┘ '
        )

        game_solver = RoundTripSolver(Grid.from_str(grid_str, type(Island)), clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_evil_3eq82(self):
        """https://gridpuzzle.com/round-trip/3eq82"""
        grid_str = (
            ' ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  · '
        )
        clues = {
            Direction.down(): [2, _, _, _, _],
            Direction.left(): [4, _, 3, _, _],
            Direction.up(): [_, 2, _, 5, _],
            Direction.right(): [_, 2, _, 4, _],
        }

        expected_solution_string = (
            ' ┌────────┐  · \n'
            ' └──┐  ·  │  · \n'
            ' ┌──┘  ┌──┼──┐ \n'
            ' │  ┌──┼──┼──┘ \n'
            ' └──┘  └──┘  · '
        )

        game_solver = RoundTripSolver(Grid.from_str(grid_str, type(Island)), clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_evil_316vk(self):
        """https://gridpuzzle.com/round-trip/316vk"""
        grid_str = (
            ' ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  · '
        )
        clues = {
            Direction.down(): [_, _, 4, _, _],
            Direction.left(): [_, 2, 0, 5, _],
            Direction.up(): [_, _, _, _, _],
            Direction.right(): [5, _, _, _, _],
        }

        expected_solution_string = (
            ' ┌───────────┐ \n'
            ' └─────┐  ┌──┘ \n'
            ' ·  ·  │  │  · \n'
            ' ┌─────┼──┼──┐ \n'
            ' └─────┘  └──┘ '
        )

        game_solver = RoundTripSolver(Grid.from_str(grid_str, type(Island)), clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_evil_31716(self):
        """https://gridpuzzle.com/round-trip/31716"""
        grid_str = (
            ' ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  · '
        )
        clues = {
            Direction.down(): [6, 2, _, _, 4, 3],
            Direction.left(): [3, _, 3, _, _, 2],
            Direction.up(): [_, _, 2, 2, 2, _],
            Direction.right(): [_, _, _, 3, _, _],
        }

        expected_solution_string = (
            ' ┌──┐  ┌─────┐  · \n'
            ' │  └──┼──┐  │  · \n'
            ' │  ┌──┘  └──┼──┐ \n'
            ' │  │  ┌─────┘  │ \n'
            ' │  │  └──┐  ┌──┘ \n'
            ' └──┘  ·  └──┘  · '
        )

        game_solver = RoundTripSolver(Grid.from_str(grid_str, type(Island)), clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_evil_1y879(self):
        """https://gridpuzzle.com/round-trip/1y879"""
        grid_str = (
            ' ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  · '
        )
        clues = {
            Direction.down(): [3, 6, 3, 2, 4, 4, 3, 2],
            Direction.left(): [_, 6, _, _, _, 3, _, _],
            Direction.up(): [2, _, _, 3, 2, 3, 5, 3],
            Direction.right(): [5, _, _, _, 5, _, 3, _],
        }

        expected_solution_string = (
            ' ┌───────────┐  ┌──┐  · \n'
            ' │  ·  ┌─────┼──┼──┼──┐ \n'
            ' └──┐  │  ·  │  │  └──┘ \n'
            ' ┌──┼──┘  ┌──┘  └──┐  · \n'
            ' │  │  ·  └────────┼──┐ \n'
            ' └──┼──┐  ┌─────┐  │  │ \n'
            ' ┌──┼──┘  │  ┌──┼──┼──┘ \n'
            ' └──┘  ·  └──┘  └──┘  · '
        )

        game_solver = RoundTripSolver(Grid.from_str(grid_str, type(Island)), clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_evil_20e6d(self):
        """https://gridpuzzle.com/round-trip/20e6d"""
        grid_str = (
            ' ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  · '
        )
        clues = {
            Direction.down(): [2, 3, _, _, _, 2, 3, 2],
            Direction.left(): [_, 4, 4, 4, 4, _, _, _],
            Direction.up(): [_, _, 3, _, 4, 3, _, 3],
            Direction.right(): [2, _, 3, _, 3, 5, 3, _],
        }

        expected_solution_string = (
            ' ·  ·  ·  ┌──┐  ┌──┐  · \n'
            ' ┌──┐  ┌──┼──┼──┘  │  · \n'
            ' └──┼──┘  └──┼─────┘  · \n'
            ' ┌──┘  ·  ·  └────────┐ \n'
            ' └─────┐  ·  ┌────────┘ \n'
            ' ·  ┌──┼─────┼──┐  ┌──┐ \n'
            ' ┌──┼──┘  ┌──┼──┼──┘  │ \n'
            ' └──┘  ·  └──┘  └─────┘ '
        )

        game_solver = RoundTripSolver(Grid.from_str(grid_str, type(Island)), clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_evil_094d8(self):
        """https://gridpuzzle.com/round-trip/094d8"""
        grid_str = (
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  · \n'
            ' ·  ·  ·  ·  ·  ·  ·  ·  ·  · '
        )
        clues = {
            Direction.down(): [6, 6, 7, 3, _, _, 5, 4, 3, _],
            Direction.left(): [_, _, 4, 2, 2, _, 3, _, 2, _],
            Direction.up(): [_, _, 3, 3, _, _, 4, 3, 3, 3],
            Direction.right(): [_, 4, _, 3, 4, 10, _, _, 4, 2, _],
        }

        expected_solution_string = (
            ' ┌─────┐  ┌─────┐  ┌──┐  ┌──┐ \n'
            ' │  ┌──┼──┼──┐  │  │  │  │  │ \n'
            ' │  │  │  └──┘  └──┼──┼──┘  │ \n'
            ' │  │  │  ┌─────┐  │  └──┐  │ \n'
            ' │  │  │  └─────┼──┘  ·  └──┘ \n'
            ' └──┼──┼────────┼───────────┐ \n'
            ' ┌──┘  └──┐  ┌──┼──┐  ·  ·  │ \n'
            ' └──┐  ┌──┼──┼──┼──┼──┐  ┌──┘ \n'
            ' ┌──┼──┼──┘  └──┘  │  │  │  · \n'
            ' └──┘  └───────────┘  └──┘  · '
        )

        game_solver = RoundTripSolver(Grid.from_str(grid_str, type(Island)), clues)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


