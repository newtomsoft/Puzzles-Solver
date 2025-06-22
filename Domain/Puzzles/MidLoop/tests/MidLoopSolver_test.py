import unittest
from unittest import TestCase

from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Puzzles.MidLoop.MidLoopSolver import MidLoopSolver

_ = 0


class MidLoopSolverTests(TestCase):
    def test_minimal_solution_3x3(self):
        grid_size = (3, 3)
        circles_positions = {1: Position(1, 0), 2: Position(1, 2)}
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

    def test_solution_with_edge_vertical_symetry_3x3(self):
        grid_size = (3, 3)
        circles_positions = {1: Position(0.5, 0), 2: Position(1, 2)}
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

    def test_solution_with_edge_horizontal_symetry_3x3(self):
        grid_size = (3, 3)
        circles_positions = {1: Position(0, 0.5), 2: Position(2, 1)}
        expected_solution_str = (
            ' ┌──┐    \n'
            ' │  └──┐ \n'
            ' └─────┘ '
        )
        game_solver = MidLoopSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_6x6_0xm72(self):
        #  https://gridpuzzle.com/mid-loop/0xm72
        grid_size = (6, 6)
        circles_positions = {
            1: Position(0.5, 4.0), 2: Position(1.0, 3.0), 3: Position(2.0, 3.5), 4: Position(2.5, 0.0),
            5: Position(3.5, 4.0), 6: Position(4.0, 5.0), 7: Position(4.5, 1.0), 8: Position(4.5, 2.0)
        }
        expected_solution_str = (
            ' ┌─────┐     ┌──┐ \n'
            ' │     └─────┘  │ \n'
            ' │     ┌────────┘ \n'
            ' │     └──┐  ┌──┐ \n'
            ' │  ┌──┐  └──┘  │ \n'
            ' └──┘  └────────┘ '
        )
        game_solver = MidLoopSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_7x7_168q6(self):
        #  https://gridpuzzle.com/mid-loop/168q6
        grid_size = (7, 7)
        circles_positions = {
            1: Position(0.0, 1.0), 2: Position(0.0, 4.0), 3: Position(1.0, 0.5), 4: Position(1.0, 3.0), 5: Position(2.5, 1.0), 6: Position(2.5, 6.0),
            7: Position(3.0, 3.5), 8: Position(3.0, 5.0), 9: Position(4.0, 3.0), 10: Position(6.0, 0.5), 11: Position(6.0, 4.0)
        }
        expected_solution_str = (
            ' ┌─────┐  ┌─────┐    \n'
            ' └──┐  │  │     └──┐ \n'
            '    │  └──┘  ┌──┐  │ \n'
            '    │     ┌──┘  │  │ \n'
            ' ┌──┘     │     └──┘ \n'
            ' │  ┌──┐  └────────┐ \n'
            ' └──┘  └───────────┘ '
        )
        game_solver = MidLoopSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
