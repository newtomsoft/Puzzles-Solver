import unittest
from unittest import TestCase

from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.MidLoop.MidLoopSolver import MidLoopSolver

_ = 0


class MidLoopSolverTests(TestCase):
    def test_minimal_solution_3x3(self):
        grid_size = (3, 3)
        circles_positions = {1: Position(1, 0), 2: Position(1, 2)}
        expected_solution_str = (
            ' ┌─────┐ \n'
            ' │  ·  │ \n'
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
            ' ·  └──┘ '
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
            ' ┌──┐  · \n'
            ' │  └──┐ \n'
            ' └─────┘ '
        )
        game_solver = MidLoopSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_6x6_0xm72(self):
        """https://gridpuzzle.com/mid-loop/0xm72"""
        grid_size = (6, 6)
        circles_positions = {
            1: Position(0.5, 4.0), 2: Position(1.0, 3.0), 3: Position(2.0, 3.5), 4: Position(2.5, 0.0),
            5: Position(3.5, 4.0), 6: Position(4.0, 5.0), 7: Position(4.5, 1.0), 8: Position(4.5, 2.0)
        }
        expected_solution_str = (
            ' ┌─────┐  ·  ┌──┐ \n'
            ' │  ·  └─────┘  │ \n'
            ' │  ·  ┌────────┘ \n'
            ' │  ·  └──┐  ┌──┐ \n'
            ' │  ┌──┐  └──┘  │ \n'
            ' └──┘  └────────┘ '
        )
        game_solver = MidLoopSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_7x7_168q6(self):
        """https://gridpuzzle.com/mid-loop/168q6"""
        grid_size = (7, 7)
        circles_positions = {
            1: Position(0.0, 1.0), 2: Position(0.0, 4.0), 3: Position(1.0, 0.5), 4: Position(1.0, 3.0), 5: Position(2.5, 1.0), 6: Position(2.5, 6.0),
            7: Position(3.0, 3.5), 8: Position(3.0, 5.0), 9: Position(4.0, 3.0), 10: Position(6.0, 0.5), 11: Position(6.0, 4.0)
        }
        expected_solution_str = (
            ' ┌─────┐  ┌─────┐  · \n'
            ' └──┐  │  │  ·  └──┐ \n'
            ' ·  │  └──┘  ┌──┐  │ \n'
            ' ·  │  ·  ┌──┘  │  │ \n'
            ' ┌──┘  ·  │  ·  └──┘ \n'
            ' │  ┌──┐  └────────┐ \n'
            ' └──┘  └───────────┘ '
        )
        game_solver = MidLoopSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    @unittest.skip("Temp")
    def test_solution_8x8_0z44g(self):
        """https://gridpuzzle.com/mid-loop/0z44g"""
        grid_size = (8, 8)
        circles_positions = {
            1: Position(0.0, 1.5), 2: Position(0.0, 5.5), 3: Position(1.5, 7.0), 4: Position(2.0, 0.0), 5: Position(2.0, 3.0), 6: Position(3.0, 4.0),
            7: Position(3.0, 6.0), 8: Position(4.0, 2.5), 9: Position(4.0, 5.0), 10: Position(5.0, 1.0), 11: Position(5.0, 2.0), 12: Position(5.5, 7.0),
            13: Position(6.0, 0.5), 14: Position(7.0, 3.5)
        }
        expected_solution_str = (
            ' ┌────────┐  ┌────────┐ \n'
            ' │  ·  ·  │  │  ·  ·  │ \n'
            ' │  ·  ·  │  │  ·  ·  │ \n'
            ' │  ·  ·  │  │  ┌─────┘ \n'
            ' └──┐  ┌──┘  │  │  ┌──┐ \n'
            ' ·  │  │  ·  │  └──┘  │ \n'
            ' ┌──┘  └─────┘  ·  ·  │ \n'
            ' └────────────────────┘ '
        )
        game_solver = MidLoopSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_9x9(self):
        grid_size = (9, 9)
        circles_positions = {
            1: Position(0.0, 2.0), 2: Position(0.5, 6.0), 3: Position(0.5, 7.0), 4: Position(1.0, 0.0), 5: Position(1.0, 5.0), 6: Position(2.0, 1.0),
            7: Position(2.0, 5.5), 8: Position(2.5, 3.0), 9: Position(2.5, 8.0), 10: Position(3.5, 0.0), 11: Position(5.5, 1.0), 12: Position(6.0, 2.5),
            13: Position(6.5, 4.0), 14: Position(6.5, 5.0), 15: Position(7.0, 7.5), 16: Position(7.5, 0.0), 17: Position(7.5, 8.0), 18: Position(8.0, 2.0),
            19: Position(8.0, 6.5)
        }
        expected_solution_str = (
            ' ┌───────────┐  ┌──┐  ┌──┐ \n'
            ' │  ·  ·  ·  │  │  └──┘  │ \n'
            ' └─────┐  ┌──┘  └──┐  ·  │ \n'
            ' ┌─────┘  └────────┘  ·  │ \n'
            ' └──┐  ┌───────────┐  ·  │ \n'
            ' ·  │  │  ┌──┐  ┌──┘  ┌──┘ \n'
            ' ·  │  └──┘  │  │  ·  │  · \n'
            ' ┌──┘  ·  ·  │  │  ·  └──┐ \n'
            ' └───────────┘  └────────┘ '
        )
        game_solver = MidLoopSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_10x10_0mdr8(self):
        """https://gridpuzzle.com/mid-loop/0mdr8"""
        grid_size = (10, 10)
        circles_positions = {
            1: Position(0.0, 3.0), 2: Position(0.0, 8.5), 3: Position(0.5, 6.0), 4: Position(1.0, 8.0), 5: Position(2.0, 3.0), 6: Position(2.0, 7.0),
            7: Position(2.5, 2.0), 8: Position(3.0, 1.0), 9: Position(4.0, 7.5), 10: Position(4.5, 0.0), 11: Position(5.0, 1.0), 12: Position(5.0, 3.0),
            13: Position(5.0, 5.0), 14: Position(5.0, 7.5), 15: Position(6.5, 0.0), 16: Position(6.5, 7.0), 17: Position(7.0, 4.0), 18: Position(7.0, 9.0),
            19: Position(7.5, 2.0), 20: Position(8.0, 6.0), 21: Position(9.0, 1.5), 22: Position(9.0, 4.5), 23: Position(9.0, 7.5)
        }
        expected_solution_str = (
            ' ┌─────────────────┐  ·  ┌──┐ \n'
            ' │  ·  ·  ·  ·  ┌──┘  ·  │  │ \n'
            ' └──┐  ┌─────┐  │  ┌─────┘  │ \n'
            ' ·  │  └──┐  │  └──┘  ·  ·  │ \n'
            ' ┌──┘  ·  │  └──┐  ┌────────┘ \n'
            ' └─────┐  │  ·  │  └────────┐ \n'
            ' ┌─────┘  │  ·  └─────┐  ·  │ \n'
            ' └─────┐  └─────┐  ┌──┘  ·  │ \n'
            ' ┌─────┘  ┌──┐  │  │  ·  ·  │ \n'
            ' └────────┘  └──┘  └────────┘ '
        )
        game_solver = MidLoopSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_12x12_0deww(self):
        """https://gridpuzzle.com/mid-loop/0deww"""
        grid_size = (12, 12)
        circles_positions = {
            1: Position(0.0, 1.0), 2: Position(0.0, 9.5), 3: Position(1.0, 3.5), 4: Position(1.0, 6.0), 5: Position(1.0, 7.5), 6: Position(1.5, 0.0),
            7: Position(1.5, 11.0), 8: Position(2.0, 7.5), 9: Position(3.0, 2.0), 10: Position(3.0, 5.0), 11: Position(3.0, 9.0), 12: Position(3.5, 4.0),
            13: Position(4.0, 3.5), 14: Position(4.0, 8.0), 15: Position(5.0, 0.5), 16: Position(5.0, 6.0), 17: Position(5.0, 10.5), 18: Position(6.0, 4.5),
            19: Position(6.0, 8.5), 20: Position(6.0, 11.0), 21: Position(6.5, 1.0), 22: Position(6.5, 6.0), 23: Position(6.5, 10.0), 24: Position(8.0, 3.0),
            25: Position(8.0, 9.0), 26: Position(8.5, 5.0), 27: Position(9.0, 0.0), 28: Position(9.0, 2.5), 29: Position(9.0, 4.5), 30: Position(9.5, 11.0),
            31: Position(10.0, 0.5), 32: Position(10.0, 3.0), 33: Position(10.0, 4.0), 34: Position(10.0, 5.5), 35: Position(10.0, 9.0),
            36: Position(10.0, 10.0), 37: Position(10.5, 5.0), 38: Position(11.0, 1.5), 39: Position(11.0, 7.0), 40: Position(11.0, 10.5)
        }
        expected_solution_str = (
            ' ┌─────┐  ·  ·  ·  ┌──┐  ┌────────┐ \n'
            ' │  ·  └────────┐  │  └──┘  ·  ·  │ \n'
            ' │  ·  ·  ·  ·  │  └────────┐  ·  │ \n'
            ' └───────────┐  │  ·  ·  ·  │  ┌──┘ \n'
            ' ┌─────┐  ┌──┘  │  ·  ┌─────┘  │  · \n'
            ' └──┐  │  │  ·  └─────┘  ·  ·  └──┐ \n'
            ' ·  │  │  └────────┐  ┌────────┐  │ \n'
            ' ·  │  │  ·  ┌─────┘  │  ·  ·  └──┘ \n'
            ' ┌──┘  └─────┘  ┌──┐  └───────────┐ \n'
            ' │  ·  ┌──┐  ┌──┘  │  ·  ·  ┌──┐  │ \n'
            ' └──┐  │  │  │  ┌──┘  ·  ·  │  │  │ \n'
            ' ·  └──┘  └──┘  └───────────┘  └──┘ '
        )
        game_solver = MidLoopSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)


    @unittest.skip("This test is skipped because in the current implementation, the solver does not support this puzzle.")
    def test_solution_12x12_0dp48(self):
        """https://gridpuzzle.com/mid-loop/0dp48"""
        grid_size = (12, 12)
        circles_positions = {
            1: Position(0.0, 3.0), 2: Position(1.0, 0.0), 3: Position(1.0, 5.5), 4: Position(1.0, 7.0), 5: Position(1.0, 8.0), 6: Position(1.0, 9.0),
            7: Position(2.5, 6.0), 8: Position(3.0, 8.0), 9: Position(3.0, 11.0), 10: Position(4.0, 0.5), 11: Position(4.0, 4.0), 12: Position(4.0, 5.5),
            13: Position(4.0, 10.0), 14: Position(5.0, 0.0), 15: Position(5.0, 8.5), 16: Position(5.5, 7.0), 17: Position(6.0, 2.0), 18: Position(6.0, 5.5),
            19: Position(6.0, 9.5), 20: Position(6.5, 4.0), 21: Position(7.0, 6.0), 22: Position(7.5, 1.0), 23: Position(7.5, 8.0), 24: Position(8.0, 3.0),
            25: Position(8.0, 10.0), 26: Position(8.5, 5.0), 27: Position(8.5, 9.0), 28: Position(9.0, 2.5), 29: Position(9.0, 7.0), 30: Position(9.0, 8.5),
            31: Position(9.5, 11.0), 32: Position(10.0, 5.5), 33: Position(11.0, 3.0), 34: Position(11.0, 9.0)
        }
        expected_solution_str = (
            ' ┌─────┐  ┌─────┐    \n'
            ' └──┐  │  │  ·  └──┐ \n'
            '    │  └──┘  ┌──┐  │ \n'
            '    │  ·  ┌──┘  │  │ \n'
            ' ┌──┘  ·  │     └──┘ \n'
            ' │  ┌──┐  └────────┐ \n'
            ' └──┘  └───────────┘ '
        )
        game_solver = MidLoopSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    @unittest.skip("Temp")
    def test_solution_12x12_a(self):
        grid_size = (12, 12)
        circles_positions = {
            1: Position(0.0, 2.5), 2: Position(0.0, 8.0), 3: Position(0.5, 5.0), 4: Position(1.0, 6.0), 5: Position(1.0, 10.0), 6: Position(1.5, 4.0),
            7: Position(2.0, 0.0), 8: Position(2.0, 2.0), 9: Position(2.0, 7.5), 10: Position(2.0, 11.0), 11: Position(3.0, 3.0), 12: Position(3.0, 6.0),
            13: Position(3.5, 4.0), 14: Position(3.5, 9.0), 15: Position(4.0, 3.5), 16: Position(4.0, 10.0), 17: Position(5.0, 0.5), 18: Position(5.0, 2.0),
            19: Position(5.0, 4.0), 20: Position(5.0, 7.5), 21: Position(6.0, 6.0), 22: Position(6.0, 8.0), 23: Position(6.5, 7.0), 24: Position(7.0, 3.5),
            25: Position(7.5, 9.0), 26: Position(8.0, 4.5), 27: Position(8.0, 10.0), 28: Position(8.5, 1.0), 29: Position(8.5, 7.0), 30: Position(9.0, 6.5),
            31: Position(9.0, 10.5), 32: Position(10.0, 2.0), 33: Position(10.0, 3.0), 34: Position(10.0, 8.0), 35: Position(10.5, 0.0),
            36: Position(11.0, 5.0),
            37: Position(11.0, 9.0)
        }
        expected_solution_str = (
            ' ┌──────────────┐  ·  ┌─────┐  ·  · \n'
            ' │  ·  ┌─────┐  └─────┘  ·  └─────┐ \n'
            ' │  ·  │  ·  └──┐  ┌────────┐  ·  │ \n'
            ' │  ·  └─────┐  │  │  ·  ·  │  ┌──┘ \n'
            ' └─────┐  ┌──┘  └──┘  ·  ·  │  │  · \n'
            ' ┌──┐  │  └─────┐  ┌────────┘  └──┐ \n'
            ' │  └──┘  ·  ·  │  │  ┌─────┐  ·  │ \n'
            ' └──┐  ┌────────┘  └──┘  ·  │  ┌──┘ \n'
            ' ·  │  └──────────────┐  ·  │  │  · \n'
            ' ·  │  ┌──┐  ·  ·  ┌──┘  ┌──┘  └──┐ \n'
            ' ┌──┘  │  │  ·  ·  └──┐  │  ·  ┌──┘ \n'
            ' └─────┘  └───────────┘  └─────┘  · '
        )
        game_solver = MidLoopSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    @unittest.skip("Temp")
    def test_solution_12x12_4mg5g(self):
        """https://gridpuzzle.com/mid-loop/4mg5g"""
        grid_size = (12, 12)
        circles_positions = {
            1: Position(0.0, 2.5), 2: Position(0.0, 8.0), 3: Position(0.5, 5.0), 4: Position(1.0, 6.0), 5: Position(1.0, 10.0), 6: Position(1.5, 4.0),
            7: Position(2.0, 0.0), 8: Position(2.0, 2.0), 9: Position(2.0, 7.5), 10: Position(2.0, 11.0), 11: Position(3.0, 3.0), 12: Position(3.0, 6.0),
            13: Position(3.5, 4.0), 14: Position(3.5, 9.0), 15: Position(4.0, 3.5), 16: Position(4.0, 10.0), 17: Position(5.0, 0.5), 18: Position(5.0, 2.0),
            19: Position(5.0, 4.0), 20: Position(5.0, 7.5), 21: Position(6.0, 6.0), 22: Position(6.0, 8.0), 23: Position(6.5, 7.0), 24: Position(7.0, 3.5),
            25: Position(7.5, 9.0), 26: Position(8.0, 4.5), 27: Position(8.0, 10.0), 28: Position(8.5, 1.0), 29: Position(8.5, 7.0), 30: Position(9.0, 6.5),
            31: Position(9.0, 10.5), 32: Position(10.0, 2.0), 33: Position(10.0, 3.0), 34: Position(10.0, 8.0), 35: Position(10.5, 0.0),
            36: Position(11.0, 5.0), 37: Position(11.0, 9.5)
        }
        game_solver = MidLoopSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        self.assertNotEqual(IslandGrid.empty(), solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_12x12_5j2e0(self):
        """https://gridpuzzle.com/mid-loop/5j2e0"""
        grid_size = (12, 12)
        circles_positions = {
            1: Position(0.0, 2.0), 2: Position(0.0, 6.0), 3: Position(0.0, 9.5), 4: Position(1.0, 4.0), 5: Position(1.0, 7.5), 6: Position(2.0, 2.5),
            7: Position(2.0, 6.0), 8: Position(2.0, 11.0), 9: Position(2.5, 9.0), 10: Position(3.0, 4.5), 11: Position(4.0, 2.0), 12: Position(4.0, 4.5),
            13: Position(4.0, 10.0), 14: Position(5.0, 1.5), 15: Position(5.0, 6.0), 16: Position(5.0, 10.0), 17: Position(5.5, 1.0), 18: Position(6.0, 3.5),
            19: Position(6.5, 11.0), 20: Position(7.0, 2.0), 21: Position(7.0, 4.0), 22: Position(7.0, 8.5), 23: Position(7.5, 5.0), 24: Position(7.5, 6.0),
            25: Position(8.0, 4.0), 26: Position(8.0, 9.0), 27: Position(9.0, 4.5), 28: Position(9.0, 10.5), 29: Position(10.0, 0.0), 30: Position(10.0, 5.0),
            31: Position(10.0, 11.0), 32: Position(10.5, 4.0), 33: Position(10.5, 6.0), 34: Position(11.0, 2.0), 35: Position(11.0, 9.5)
        }
        expected_solution_str = (
            ' ┌───────────┐  ┌─────┐  ┌────────┐ \n'
            ' │  ·  ·  ·  │  └──┐  └──┘  ·  ·  │ \n'
            ' │  ┌────────┘  ·  │  ┌─────┐  ·  │ \n'
            ' │  │  ·  ┌────────┘  │  ┌──┘  ·  │ \n'
            ' │  └─────┘  ┌──┐  ·  │  │  ┌─────┘ \n'
            ' │  ┌──┐  ·  │  └─────┘  │  └─────┐ \n'
            ' └──┘  │  ┌──┘  ·  ┌──┐  │  ·  ·  │ \n'
            ' ·  ·  │  └─────┐  │  │  └──┐  ·  │ \n'
            ' ·  ·  │  ┌─────┘  │  │  ·  │  ┌──┘ \n'
            ' ┌─────┘  └────────┘  │  ┌──┘  └──┐ \n'
            ' │  ·  ·  ·  ┌─────┐  │  │  ·  ·  │ \n'
            ' └───────────┘  ·  └──┘  └────────┘ '
        )
        game_solver = MidLoopSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_15x15_0gmw8(self):
        """https://gridpuzzle.com/mid-loop/0gmw8"""
        grid_size = (15, 15)
        circles_positions = {
            1: Position(0.0, 1.5), 2: Position(0.0, 4.5), 3: Position(0.0, 8.5), 4: Position(0.0, 13.0), 5: Position(0.5, 0.0), 6: Position(1.0, 1.0),
            7: Position(1.0, 4.0), 8: Position(1.0, 8.0), 9: Position(1.0, 10.5), 10: Position(1.0, 12.0), 11: Position(1.5, 3.0), 12: Position(1.5, 14.0),
            13: Position(2.5, 9.0), 14: Position(3.0, 0.0), 15: Position(3.0, 1.5), 16: Position(3.0, 7.0), 17: Position(3.0, 10.5), 18: Position(3.0, 13.0),
            19: Position(3.5, 1.0), 20: Position(4.0, 2.0), 21: Position(4.0, 5.0), 22: Position(4.0, 8.0), 23: Position(4.0, 10.0), 24: Position(4.5, 6.0),
            25: Position(4.5, 11.0), 26: Position(5.0, 3.5), 27: Position(5.0, 9.5), 28: Position(5.0, 12.0), 29: Position(5.5, 13.0), 30: Position(6.0, 1.0),
            31: Position(6.0, 6.5), 32: Position(6.0, 11.0), 33: Position(7.0, 4.5), 34: Position(7.0, 8.0), 35: Position(7.0, 10.0), 36: Position(7.0, 13.0),
            37: Position(7.5, 2.0), 38: Position(7.5, 4.0), 39: Position(8.0, 3.5), 40: Position(8.0, 6.5), 41: Position(8.0, 14.0), 42: Position(8.5, 5.0),
            43: Position(9.0, 2.5), 44: Position(9.0, 12.0), 45: Position(9.5, 3.0), 46: Position(9.5, 10.0), 47: Position(10.0, 6.5), 48: Position(10.0, 8.0),
            49: Position(10.0, 12.0), 50: Position(10.5, 7.0), 51: Position(10.5, 14.0), 52: Position(11.0, 8.5), 53: Position(11.0, 13.0),
            54: Position(11.5, 0.0), 55: Position(11.5, 1.0), 56: Position(11.5, 4.0), 57: Position(11.5, 10.0), 58: Position(11.5, 12.0),
            59: Position(12.0, 2.0), 60: Position(12.0, 7.5), 61: Position(12.0, 9.5), 62: Position(12.0, 13.0), 63: Position(13.0, 4.0),
            64: Position(13.0, 7.0), 65: Position(13.0, 8.0), 66: Position(13.0, 14.0), 67: Position(13.5, 1.0), 68: Position(13.5, 2.0),
            69: Position(13.5, 10.0), 70: Position(13.5, 12.0), 71: Position(13.5, 13.0), 72: Position(14.0, 3.5), 73: Position(14.0, 8.5),
            74: Position(14.0, 11.0)
        }
        expected_solution_str = (
            ' ┌────────┐  ┌──┐  ┌──────────────┐  ┌─────┐ \n'
            ' └─────┐  │  │  └──┘  ┌─────┐  ┌──┘  │  ·  │ \n'
            ' ┌─────┘  │  └──┐  ┌──┘  ·  │  │  ┌──┘  ·  │ \n'
            ' │  ┌──┐  └─────┘  └─────┐  │  └──┘  ┌─────┘ \n'
            ' └──┘  │  ·  ┌─────┐  ·  │  └─────┐  └─────┐ \n'
            ' ┌─────┘  ┌──┘  ·  └─────┘  ┌──┐  └─────┐  │ \n'
            ' └─────┐  │  ·  ┌────────┐  │  └─────┐  └──┘ \n'
            ' ·  ·  │  │  ┌──┘  ·  ·  │  └─────┐  └─────┐ \n'
            ' ·  ·  │  └──┘  ┌────────┘  ┌─────┘  ·  ·  │ \n'
            ' ┌──┐  └──┐  ┌──┘  ┌─────┐  │  ┌───────────┘ \n'
            ' │  └─────┘  └──┐  └──┐  │  │  └───────────┐ \n'
            ' │  ┌────────┐  └─────┘  └──┘  ┌──┐  ┌─────┘ \n'
            ' │  └─────┐  └─────┐  ┌──┐  ┌──┘  │  └─────┐ \n'
            ' │  ┌──┐  └─────┐  │  │  │  │  ┌──┘  ┌──┐  │ \n'
            ' └──┘  └────────┘  └──┘  └──┘  └─────┘  └──┘ '
        )
        game_solver = MidLoopSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

    def test_solution_15x15_11pjk(self):
        """https://gridpuzzle.com/mid-loop/11pjk"""
        grid_size = (15, 15)
        circles_positions = {
            1: Position(0.0, 1.5), 2: Position(0.0, 5.0), 3: Position(0.0, 8.0), 4: Position(0.5, 6.0), 5: Position(1.0, 3.0), 6: Position(1.0, 5.5),
            7: Position(1.5, 0.0), 8: Position(1.5, 9.0), 9: Position(1.5, 10.0), 10: Position(1.5, 11.0), 11: Position(2.0, 3.5), 12: Position(2.0, 6.0),
            13: Position(2.0, 13.0), 14: Position(2.0, 14.0), 15: Position(2.5, 1.0), 16: Position(3.0, 5.5), 17: Position(3.5, 3.0), 18: Position(4.0, 0.5),
            19: Position(4.0, 5.0), 20: Position(4.0, 12.0), 21: Position(4.5, 1.0), 22: Position(4.5, 8.0), 23: Position(4.5, 10.0), 24: Position(5.0, 3.5),
            25: Position(5.0, 7.0), 26: Position(5.0, 12.0), 27: Position(6.0, 3.0), 28: Position(6.5, 5.0), 29: Position(6.5, 13.0), 30: Position(7.0, 9.0),
            31: Position(8.0, 3.0), 32: Position(8.0, 8.5), 33: Position(8.5, 11.0), 34: Position(8.5, 14.0), 35: Position(9.0, 2.0), 36: Position(9.5, 6.0),
            37: Position(10.0, 1.5), 38: Position(10.0, 5.0), 39: Position(10.0, 13.0), 40: Position(10.5, 4.0), 41: Position(10.5, 9.0),
            42: Position(11.0, 3.0), 43: Position(11.0, 13.0), 44: Position(11.5, 7.0), 45: Position(11.5, 12.0), 46: Position(12.0, 0.0),
            47: Position(12.0, 1.5), 48: Position(12.0, 5.5), 49: Position(12.0, 8.0), 50: Position(12.5, 11.0), 51: Position(13.0, 2.0),
            52: Position(13.0, 5.0), 53: Position(13.0, 7.5), 54: Position(13.0, 9.5), 55: Position(13.0, 14.0), 56: Position(14.0, 0.5),
            57: Position(14.0, 7.5), 58: Position(14.0, 12.5)
        }
        expected_solution_str = (
            ' ┌────────┐  ┌─────┐  ┌─────┐  ┌──┐  ┌─────┐ \n'
            ' │  ·  ·  │  │  ┌──┘  │  ·  │  │  │  └──┐  │ \n'
            ' │  ┌──┐  └──┘  └─────┘  ·  │  │  │  ·  │  │ \n'
            ' └──┘  │  ┌──────────────┐  └──┘  └─────┘  │ \n'
            ' ┌──┐  │  └───────────┐  │  ·  ┌───────────┘ \n'
            ' │  └──┘  ┌──┐  ·  ·  │  │  ·  └───────────┐ \n'
            ' └─────┐  │  │  ┌─────┘  └──┐  ┌────────┐  │ \n'
            ' ┌──┐  └──┘  └──┘  ┌─────┐  │  │  ┌──┐  └──┘ \n'
            ' │  └───────────┐  │  ·  └──┘  │  │  └─────┐ \n'
            ' └───────────┐  │  │  ·  ┌─────┘  │  ┌─────┘ \n'
            ' ┌────────┐  │  │  │  ┌──┘  ┌─────┘  └─────┐ \n'
            ' │  ·  ·  │  │  │  │  │  ┌──┘  ┌──┐  ┌─────┘ \n'
            ' │  ┌──┐  └──┘  └──┘  │  │  ·  │  │  └─────┐ \n'
            ' │  │  │  ·  ┌─────┐  └──┘  ┌──┘  │  ·  ·  │ \n'
            ' └──┘  └─────┘  ·  └────────┘  ·  └────────┘ '
        )
        game_solver = MidLoopSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = game_solver.get_other_solution()
        self.assertEqual(IslandGrid.empty(), other_solution)

if __name__ == '__main__':
    unittest.main()
