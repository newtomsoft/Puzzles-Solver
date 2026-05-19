from unittest import TestCase

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.Rimotoejji.RimotoejjiSolver import RimotoejjiSolver

_ = ' '
D = '↓'
U = '↑'
R = '→'
L = '←'
P = '+'


class RimotoejjiSolverTest(TestCase):
    def test_puzzle_5x5_easy_1nwe9(self):
        """https://fr.gridpuzzle.com/rimotoejji/1nwe9"""
        grid = Grid([
            [_, _, _, _, _],
            [D, _, L, _, P],
            [P, _, U, _, U],
            [_, _, _, _, _],
            [P, R, P, L, L],
        ])

        expected_solution_string = (
            ' ┌──┐  ┌────────┐ \n'
            ' │  └──┘  ┌──┐  │ \n'
            ' │  ┌──┐  │  │  │ \n'
            ' │  │  └──┘  └──┘ \n'
            ' │  └───────────┐ \n'
            ' └──────────────┘ '
        )

        game_solver = RimotoejjiSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_puzzle_5x5_evil_319zk(self):
        """https://fr.gridpuzzle.com/rimotoejji/319zk"""
        grid = Grid([
                [_, _, _, _, _],
                [U, _, _, _, D],
                [_, _, D, _, _],
                [R, _, _, _, L],
                [_, _, U, _, _],
        ])

        expected_solution_string = (
           ' ┌──────────────┐ \n'
           ' │  ┌────────┐  │ \n'
           ' └──┘  ┌──┐  │  │ \n'
           ' ┌─────┘  └──┘  │ \n'
           ' │  ┌──┐  ┌──┐  │ \n'
           ' └──┘  └──┘  └──┘ '
        )

        game_solver = RimotoejjiSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_puzzle_7x7_evil_08vv1(self):
        """https://fr.gridpuzzle.com/rimotoejji/08vv1"""
        grid = Grid([
            [D, _, _, L, _, _ ,_],
            [_, _, _, _, _, _, _],
            [_, P, _, _, _, D, _],
            [D, _, _, _, _, _, _],
            [_, _, R, _, _, _, _],
            [_, _, _, _, P, _, _],
            [_, _, U, _, _, _, U],
        ])

        expected_solution_string = (
            " ┌──┐  ┌─────┐  ┌─────┐ \n"
            " │  └──┘  ┌──┘  └──┐  │ \n"
            " └──┐  ┌──┘  ┌─────┘  │ \n"
            " ┌──┘  └──┐  └──┐  ┌──┘ \n"
            " │  ┌──┐  └─────┘  └──┐ \n"
            " │  │  │  ┌──┐  ┌──┐  │ \n"
            " │  │  │  │  │  │  │  │ \n"
            " └──┘  └──┘  └──┘  └──┘ "
        )

        game_solver = RimotoejjiSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_puzzle_9x9_evil_08vv1(self):
        """https://fr.gridpuzzle.com/rimotoejji/q25ze"""
        grid = Grid([
            [D, _, _, _, R, _ ,_, _, D],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, L, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, U, L, _, _, _, R, P, _],
            [_, _, _, _, _, _, _, _, _],
            [R, _, _, _, _, _, _, _, P],
            [_, _, _, _, U, _, _, _, _],
            [_, R, P, _, _, _, R, U, _],
        ])

        expected_solution_string = (
            " ┌─────┐  ┌───────────┐  ┌──┐ \n"
            " │  ┌──┘  │  ┌─────┐  └──┘  │ \n"
            " │  └─────┘  └──┐  └─────┐  │ \n"
            " └──┐  ┌─────┐  └─────┐  └──┘ \n"
            " ┌──┘  └──┐  └─────┐  └─────┐ \n"
            " │  ┌─────┘  ┌──┐  └─────┐  │ \n"
            " │  └────────┘  │  ┌─────┘  │ \n"
            " └───────────┐  │  └──┐  ┌──┘ \n"
            " ┌───────────┘  │  ┌──┘  └──┐ \n"
            " └──────────────┘  └────────┘ "
        )

        game_solver = RimotoejjiSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_puzzle_11x11_evil_6wzdx(self):
        """https://fr.gridpuzzle.com/rimotoejji/6wzdx"""
        grid = Grid([
            [_, D, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, L, _, R, _, _, _],
            [D, _, _, P, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, U],
            [_, _, R, _, _, _, _, _, D, _, _],
            [_, _, _, _, _, _, _, _, _, _, L],
            [_, _, _, _, _, _, L, _, _, _, _],
            [U, P, _, _, _, _, _, _, _, _, _],
            [_, _, P, _, _, U, _, _, _, _, _],
            [D, _, _, _, P, _, _, _, _, _, P],
            [_, _, _, _, _, U, _, U, _, R, _],
        ])

        expected_solution_string = (
            ' ┌─────┐  ┌──┐  ┌────────┐  ┌─────┐ \n'
            ' └──┐  │  │  └──┘  ┌──┐  └──┘  ┌──┘ \n'
            ' ┌──┘  │  │  ┌─────┘  └─────┐  └──┐ \n'
            ' │  ┌──┘  │  │  ┌────────┐  └──┐  │ \n'
            ' │  │  ┌──┘  └──┘  ┌──┐  └──┐  └──┘ \n'
            ' │  │  │  ┌─────┐  │  └──┐  └─────┐ \n'
            ' │  │  └──┘  ┌──┘  └──┐  │  ┌──┐  │ \n'
            ' │  └─────┐  └──┐  ┌──┘  │  │  └──┘ \n'
            ' └─────┐  └──┐  │  │  ┌──┘  └─────┐ \n'
            ' ┌──┐  └──┐  └──┘  │  │  ┌─────┐  │ \n'
            ' │  └─────┘  ┌──┐  │  │  │  ┌──┘  │ \n'
            ' └───────────┘  └──┘  └──┘  └─────┘ '
        )

        game_solver = RimotoejjiSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_puzzle_13x13_evil_n0k49(self):
        """https://fr.gridpuzzle.com/rimotoejji/n0k49"""
        grid = Grid([
            [_, _, _, _, _, P, _, _, L, _, L, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, D],
            [D, _, _, D, _, _, P, _, D, _, _, _, _],
            [_, _, _, _, _, P, _, _, R, _, _, _, _],
            [U, _, _, _, _, L, _, R, _, _, P, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, U],
            [_, _, _, _, _, L, L, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, P, _, _, _, P, L],
            [_, R, _, _, _, _, _, _, L, _, _, _, _],
            [_, _, _, _, R, _, _, _, _, _, _, _, _],
            [R, _, _, _, _, _, _, _, P, _, _, _, _],
            [_, _, _, _, R, _, _, _, _, _, _, _, _],
            [_, _, _, R, _, _, _, L, _, _, _, R, _],
        ])

        expected_solution_string = (
            ' ┌────────────────────────────────┐  ┌──┐ \n'
            ' └──┐  ┌───────────┐  ┌────────┐  │  │  │ \n'
            ' ┌──┘  │  ┌──┐  ┌──┘  └─────┐  └──┘  │  │ \n'
            ' │  ┌──┘  │  │  │  ┌─────┐  └────────┘  │ \n'
            ' │  │  ┌──┘  └──┘  │  ┌──┘  ┌──┐  ┌──┐  │ \n'
            ' └──┘  └───────────┘  └──┐  │  │  │  │  │ \n'
            ' ┌───────────────────────┘  │  └──┘  └──┘ \n'
            ' └────────────────────┐  ┌──┘  ┌────────┐ \n'
            ' ┌──────────────┐  ┌──┘  └──┐  │  ┌─────┘ \n'
            ' └─────┐  ┌──┐  └──┘  ┌─────┘  │  └─────┐ \n'
            ' ┌─────┘  │  └─────┐  └────────┘  ┌──┐  │ \n'
            ' └──┐  ┌──┘  ┌─────┘  ┌─────┐  ┌──┘  │  │ \n'
            ' ┌──┘  │  ┌──┘  ┌──┐  └──┐  │  │  ┌──┘  │ \n'
            ' └─────┘  └─────┘  └─────┘  └──┘  └─────┘ '
        )

        game_solver = RimotoejjiSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_string, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
