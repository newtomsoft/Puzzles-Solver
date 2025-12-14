import unittest

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.TentaiShow.TentaiShowSolver import TentaiShowSolver


class TentaiShowSolverLongTests(unittest.TestCase):
    def test_solution_15x15_hard(self):  # approximately 9 seconds
        grid_size = (15, 15)
        circles_positions = {
            1: Position(0, 0.5), 2: Position(0, 5), 3: Position(0, 11.5), 4: Position(0.5, 3.5), 5: Position(0.5, 9.5), 6: Position(1, 1), 7: Position(1, 5.5),
            8: Position(1.5, 13.5),
            9: Position(2, 7), 10: Position(2, 10.5), 11: Position(2.5, 2), 12: Position(3, 4.5), 13: Position(3, 12), 14: Position(3.5, 10.5), 15: Position(4, 2.5),
            16: Position(4, 14), 17: Position(5, 0), 18: Position(5, 2), 19: Position(5, 4.5), 20: Position(5, 6.5), 21: Position(5, 8), 22: Position(5, 9),
            23: Position(5.5, 10.5), 24: Position(6, 1), 25: Position(6, 12), 26: Position(6.5, 3.5), 27: Position(7.5, 6.5), 28: Position(7.5, 9.5), 29: Position(7.5, 12.5),
            30: Position(8.5, 2.5), 31: Position(9, 0.5), 32: Position(9, 8), 33: Position(9, 13.5), 34: Position(11, 0.5), 35: Position(11, 10.5), 36: Position(11, 12),
            37: Position(11, 14), 38: Position(11.5, 5.5), 39: Position(11.5, 8), 40: Position(11.5, 13), 41: Position(12, 2.5), 42: Position(12, 4), 43: Position(12.5, 10),
            44: Position(13, 0), 45: Position(13, 7), 46: Position(13, 9), 47: Position(13, 13.5), 48: Position(14, 7), 49: Position(14, 11.5)
        }
        game_solver = TentaiShowSolver(grid_size, circles_positions)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 6, 4, 4, 2, 7, 5, 5, 5, 5, 3, 3, 8, 8],
            [6, 6, 6, 4, 4, 7, 7, 9, 9, 5, 5, 5, 5, 8, 8],
            [6, 11, 11, 11, 12, 7, 9, 9, 9, 10, 10, 10, 10, 8, 8],
            [17, 11, 11, 11, 12, 12, 9, 9, 14, 14, 14, 14, 13, 8, 8],
            [17, 15, 15, 15, 15, 12, 20, 20, 21, 22, 14, 14, 14, 14, 16],
            [17, 24, 18, 26, 19, 19, 20, 20, 21, 22, 23, 23, 29, 29, 29],
            [17, 24, 26, 26, 26, 26, 20, 20, 21, 22, 23, 23, 25, 29, 29],
            [17, 24, 26, 26, 26, 26, 27, 27, 27, 28, 28, 29, 29, 29, 29],
            [30, 30, 30, 30, 26, 27, 27, 27, 32, 28, 28, 29, 29, 29, 29],
            [31, 31, 30, 30, 30, 30, 38, 38, 32, 35, 35, 29, 29, 33, 33],
            [34, 34, 41, 41, 41, 41, 38, 38, 32, 35, 35, 29, 29, 29, 37],
            [34, 34, 41, 41, 41, 38, 38, 39, 39, 39, 35, 35, 36, 40, 37],
            [34, 34, 41, 41, 42, 38, 38, 39, 39, 39, 43, 35, 35, 40, 37],
            [44, 41, 41, 41, 38, 38, 45, 45, 45, 46, 43, 35, 35, 47, 47],
            [41, 41, 41, 41, 38, 38, 48, 48, 48, 49, 49, 49, 49, 49, 49]
        ])
        self.assertEqual(expected_solution, solution)
