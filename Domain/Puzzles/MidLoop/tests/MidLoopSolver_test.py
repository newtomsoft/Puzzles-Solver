import unittest
from unittest import TestCase

from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Puzzles.MidLoop.MidLoopSolver import MidLoopSolver

_ = 0


class MidLoopSolverTests(TestCase):
    def test_minimal_solution_3x3(self):
        grid_size = (3, 3)
        circles_positions = {1: Position(1, 0), 2: Position(1, 2) }
        expected_solution_str = (
            ' ┌─────┐ \n'
            ' │     │ \n'
            ' └─────┘ '
        )
        game_solver = MidLoopSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_with_symetry_3x3(self):
        grid_size = (3, 3)
        circles_positions = {1: Position(0.5, 0), 2: Position(1, 2) }
        expected_solution_str = (
            ' ┌─────┐ \n'
            ' └──┐  │ \n'
            '    └──┘ '
        )
        game_solver = MidLoopSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_5x5_319d0(self):
        #  https://gridpuzzle.com/mid-loop/319d0
        grid_size = (5, 5)
        circles_positions = {
            1: Position(0.0, 1.0), 2: Position(0.0, 3.5), 3: Position(0.5, 0.0), 4: Position(0.5, 2.0), 5: Position(0.5, 3.0), 6: Position(1.0, 0.5),
            7: Position(1.0, 2.5), 8: Position(1.5, 1.0), 9: Position(2.0, 0.5), 10: Position(2.0, 4.0), 11: Position(3.0, 0.0),
            12: Position(3.0, 1.5), 13: Position(3.5, 1.0), 14: Position(3.5, 2.0), 15: Position(4.0, 0.5), 16: Position(4.0, 3.0)
        }
        expected_solution_str = (
            '            \n'
            ' ┌─────┐    \n'
            ' └──┐  │    \n'
            '    └──┘    '
        )
        game_solver = MidLoopSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
