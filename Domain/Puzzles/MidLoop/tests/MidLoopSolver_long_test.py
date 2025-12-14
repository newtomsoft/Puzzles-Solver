import unittest

from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.MidLoop.MidLoopSolver import MidLoopSolver


class MidLoopSolverLongTests(unittest.TestCase):
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

