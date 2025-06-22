import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Puzzles.Linesweeper.LinesweeperSolver import LinesweeperSolver

_ = -1


class LinesweeperSolverTests(TestCase):
    def test_solution_4x4_292p8(self):
        #  https://en.gridpuzzle.com/linesweeper/292p8
        grid = Grid([
            [_, 3, _, _],
            [_, _, _, _],
            [_, _, _, _],
            [3, _, _, 2]
        ])
        expected_solution_str = (
            '            \n'
            ' ┌─────┐    \n'
            ' └──┐  │    \n'
            '    └──┘    '
        )
        game_solver = LinesweeperSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_4x4_1n690(self):
        #  https://en.gridpuzzle.com/linesweeper/1n690
        grid = Grid([
            [_, _, 3, _],
            [_, _, _, _],
            [_, 8, _, _],
            [_, _, _, 3]
        ])
        expected_solution_str = (
            '            \n'
            ' ┌────────┐ \n'
            ' │     ┌──┘ \n'
            ' └─────┘    '
        )
        game_solver = LinesweeperSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_4x4_21d85(self):
        #  https://en.gridpuzzle.com/linesweeper/21d85
        grid = Grid([
            [3, _, _, 3],
            [_, _, _, _],
            [_, _, _, _],
            [3, _, _, 3]
        ])
        expected_solution_str = (
            '    ┌──┐    \n'
            ' ┌──┘  └──┐ \n'
            ' └──┐  ┌──┘ \n'
            '    └──┘    '
        )
        game_solver = LinesweeperSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_8x8_0evdw(self):
        #  https://en.gridpuzzle.com/linesweeper/0evdw
        grid = Grid([
            [_, _, _, _, 4, _, 3, _],
            [_, 6, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, 7, _, _, _],
            [_, _, 8, _, 5, _, _, 5],
            [4, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [2, _, _, _, 5, _, _, 3],
        ])
        expected_solution_str = (
            ' ┌────────┐             \n'
            ' │        └──┐  ┌─────┐ \n'
            ' │     ┌──┐  └──┘     │ \n'
            ' │  ┌──┘  │     ┌─────┘ \n'
            ' └──┘     │     └──┐    \n'
            '    ┌─────┘        └──┐ \n'
            '    │     ┌─────┐  ┌──┘ \n'
            '    └─────┘     └──┘    '
        )
        game_solver = LinesweeperSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_10x10_0wn5r(self):
        #  https://en.gridpuzzle.com/linesweeper/0wn5r
        grid = Grid([
            [_, _, _, 5, _, _, _, 4, _, _],
            [3, _, _, _, _, 5, _, _, _, _],
            [4, _, _, _, 6, _, _, _, _, _],
            [_, _, 8, _, _, _, _, 4, _, _],
            [_, _, _, _, 6, _, _, _, _, _],
            [_, 7, _, _, 6, _, _, 8, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [4, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, 7, _, _, 5, 6, _],
            [2, _, _, _, _, _, _, _, _, _],
        ])
        expected_solution_str = (
            '    ┌──┐     ┌─────┐          \n'
            '    │  └─────┘     └────────┐ \n'
            '    └─────┐                 │ \n'
            ' ┌──┐     └────────┐        │ \n'
            ' │  └─────┐        └─────┐  │ \n'
            ' │        │     ┌──┐     │  │ \n'
            ' └─────┐  └─────┘  │  ┌──┘  │ \n'
            '    ┌──┘  ┌─────┐  └──┘     │ \n'
            '    │     │     │           │ \n'
            '    └─────┘     └───────────┘ '
        )
        game_solver = LinesweeperSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_12x12_1kkr6(self):
        #  https://en.gridpuzzle.com/linesweeper/1kkr6
        grid = Grid([
            [_, _, _, _, _, _, _, 3, _, _, _, _],
            [_, _, _, _, _, _, _, _, 6, _, 8, _],
            [4, _, 3, _, _, 6, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, 5],
            [_, _, _, _, _, _, _, _, _, 5, _, _],
            [_, _, _, _, _, _, 6, _, _, _, _, _],
            [_, 5, 6, _, 7, _, _, 6, _, 3, _, _],
            [_, _, _, _, _, 7, _, _, _, _, _, _],
            [_, 8, _, _, _, _, _, _, _, 5, _, _],
            [_, _, _, _, 8, _, 7, _, _, _, _, 5],
            [2, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, 3, _, _, 3, _, _, _, _, _],
        ])
        expected_solution_str = (
            '    ┌────────┐  ┌──┐        ┌─────┐ \n'
            '    │        └──┘  └──┐     │     │ \n'
            '    │                 └──┐  │  ┌──┘ \n'
            ' ┌──┘        ┌─────┐     └──┘  │    \n'
            ' │  ┌─────┐  │     └──┐        └──┐ \n'
            ' └──┘     │  └──┐     └──┐        │ \n'
            '          │     └──┐     │        │ \n'
            ' ┌─────┐  └──┐     │     │        │ \n'
            ' │     └─────┘  ┌──┘  ┌──┘     ┌──┘ \n'
            ' └────────┐     │     │     ┌──┘    \n'
            '          └──┐  │     └──┐  └─────┐ \n'
            '             └──┘        └────────┘ '
        )
        game_solver = LinesweeperSolver(grid)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
