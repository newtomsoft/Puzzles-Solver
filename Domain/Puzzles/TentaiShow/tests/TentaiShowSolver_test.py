import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine
from TentaiShow.TentaiShowSolver import TentaiShowSolver


class TentaiShowSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_cells_filled_by_circles(self):
        grid_size = (2, 2)
        circle_positions = {1: Position(0, 0), 2: Position(0, 1), 3: Position(1, 0), 4: Position(1, 1)}
        game_solver = TentaiShowSolver(grid_size, circle_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 2],
            [3, 4],
        ])
        self.assertEqual(expected_solution, solution)

        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_cells_filled_by_circles_horizontally_straddled(self):
        grid_size = (2, 2)
        circle_positions = {1: Position(0, 0.5), 2: Position(1, 0.5)}
        game_solver = TentaiShowSolver(grid_size, circle_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1],
            [2, 2],
        ])
        self.assertEqual(expected_solution, solution)

        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_cells_filled_by_circles_vertically_straddled(self):
        grid_size = (2, 2)
        circle_positions = {1: Position(0.5, 0), 2: Position(0.5, 1)}
        game_solver = TentaiShowSolver(grid_size, circle_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 2],
            [1, 2],
        ])
        self.assertEqual(expected_solution, solution)

        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_cells_filled_by_circles_vertically_and_horizontally_straddled(self):
        grid_size = (4, 4)
        circle_positions = {1: Position(0.5, 0.5), 2: Position(0.5, 2.5), 3: Position(2.5, 0.5), 4: Position(2.5, 2.5)}
        game_solver = TentaiShowSolver(grid_size, circle_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 2, 2],
            [1, 1, 2, 2],
            [3, 3, 4, 4],
            [3, 3, 4, 4],
        ])
        self.assertEqual(expected_solution, solution)

        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_cells_filled_by_circles_mixed_0(self):
        grid_size = (4, 4)
        circle_positions = {
            1: Position(0, 0),
            2: Position(0, 2.5),
            3: Position(0.5, 1),
            4: Position(1, 2.5),
            5: Position(1.5, 0),
            6: Position(2, 1.5),
            7: Position(2.5, 3),
            8: Position(3, 0),
            9: Position(3, 1.5),
        }
        game_solver = TentaiShowSolver(grid_size, circle_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 3, 2, 2],
            [5, 3, 4, 4],
            [5, 6, 6, 7],
            [8, 9, 9, 7]
        ])
        self.assertEqual(expected_solution, solution)

        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_cells_filled_by_circles_mixed_1(self):
        grid_size = (4, 4)
        circle_positions = {
            1: Position(0, 0),
            2: Position(0, 1.5),
            3: Position(0.5, 3),
            4: Position(1.5, 0),
            5: Position(1.5, 1.5),
            6: Position(2, 3),
            7: Position(3, 0.5),
            8: Position(3, 2.5)
        }
        game_solver = TentaiShowSolver(grid_size, circle_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 2, 2, 3],
            [4, 5, 5, 3],
            [4, 5, 5, 6],
            [7, 7, 8, 8]
        ])
        self.assertEqual(expected_solution, solution)

        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_symmetry_constraints(self):
        grid_size = (3, 2)
        circles_positions = {1: Position(1, 0), 2: Position(1, 1)}
        game_solver = TentaiShowSolver(grid_size, circles_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 2],
            [1, 2],
            [1, 2],
        ])
        self.assertEqual(expected_solution, solution)

        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_normal(self):
        grid_size = (5, 5)
        circles_positions = {
            1: Position(0, 2), 2: Position(0.5, 1), 3: Position(0.5, 4), 4: Position(1.5, 0), 5: Position(1.5, 3),
            6: Position(3, 1), 7: Position(3, 2), 8: Position(3.5, 4), 9: Position(4, 0.5)
        }
        game_solver = TentaiShowSolver(grid_size, circles_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [4, 2, 1, 5, 3],
            [4, 2, 5, 5, 3],
            [4, 7, 7, 5, 5],
            [4, 6, 7, 5, 8],
            [9, 9, 7, 7, 8],
        ])
        self.assertEqual(expected_solution, solution)

        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_5x5_hard(self):
        grid_size = (5, 5)
        circles_positions = {
            1: Position(0, 1.5), 2: Position(0, 3.5), 3: Position(1, 2), 4: Position(2, 0),
            5: Position(2.5, 2.5), 6: Position(3.5, 0.5), 7: Position(4, 3)}
        game_solver = TentaiShowSolver(grid_size, circles_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [3, 1, 1, 2, 2],
            [3, 3, 3, 3, 3],
            [4, 5, 5, 5, 3],
            [6, 6, 5, 5, 5],
            [6, 6, 7, 7, 7]
        ])
        self.assertEqual(expected_solution, solution)

        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x7_normal(self):
        grid_size = (7, 7)
        circles_positions = {
            1: Position(0.5, 6), 2: Position(1, 0), 3: Position(1, 1), 4: Position(1, 2.5), 5: Position(2.5, 4), 6: Position(3, 5.5),
            7: Position(4, 0.5), 8: Position(4.5, 2), 9: Position(4.5, 5.5), 10: Position(6, 1.5), 11: Position(6, 5)
        }
        game_solver = TentaiShowSolver(grid_size, circles_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [2, 3, 4, 4, 5, 5, 1],
            [2, 3, 4, 4, 5, 5, 1],
            [2, 3, 4, 4, 5, 5, 5],
            [7, 7, 5, 5, 5, 6, 6],
            [7, 7, 8, 5, 5, 9, 9],
            [7, 7, 8, 5, 5, 9, 9],
            [10, 10, 10, 10, 11, 11, 11]
        ])
        self.assertEqual(expected_solution, solution)

        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x7_hard(self):
        grid_size = (7, 7)
        circles_positions = {
            1: Position(0, 0.5), 2: Position(0, 3), 3: Position(1, 0.5), 4: Position(1, 2.5), 5: Position(1, 5),
            6: Position(2, 0), 7: Position(2, 1.5), 8: Position(3, 0.5), 9: Position(3, 4.5), 10: Position(4, 3),
            11: Position(4, 5), 12: Position(4.5, 1.5), 13: Position(5, 0), 14: Position(5, 4.5), 15: Position(6, 4)
        }
        game_solver = TentaiShowSolver(grid_size, circles_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 4, 2, 5, 5, 5],
            [3, 3, 4, 4, 5, 5, 5],
            [6, 7, 7, 4, 5, 5, 5],
            [8, 8, 12, 9, 9, 9, 9],
            [13, 12, 12, 10, 11, 11, 11],
            [13, 12, 12, 14, 14, 14, 14],
            [13, 12, 15, 15, 15, 15, 15]
        ])
        self.assertEqual(expected_solution, solution)

        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_normal(self):
        grid_size = (10, 10)
        circles_positions = {
            1: Position(0, 0), 2: Position(0, 2), 3: Position(0, 4), 4: Position(0, 7), 5: Position(1, 4.5), 6: Position(1, 8.5), 7: Position(2, 3),
            8: Position(2.5, 0.5), 9: Position(2.5, 5), 10: Position(2.5, 7.5), 11: Position(3, 6), 12: Position(3.5, 3), 13: Position(4, 7), 14: Position(4.5, 9),
            15: Position(5, 2.5), 16: Position(5, 4), 17: Position(5, 8), 18: Position(6.5, 1), 19: Position(6.5, 4.5), 20: Position(7.5, 6.5), 21: Position(8, 0),
            22: Position(8.5, 8), 23: Position(8.5, 9), 24: Position(9, 1), 25: Position(9, 7)
        }
        game_solver = TentaiShowSolver(grid_size, circles_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 8, 2, 5, 3, 4, 4, 4, 4, 4],
            [8, 8, 7, 5, 5, 5, 5, 10, 6, 6],
            [8, 8, 7, 7, 7, 9, 5, 10, 10, 14],
            [8, 8, 12, 12, 7, 9, 11, 10, 10, 14],
            [8, 8, 15, 12, 12, 19, 19, 13, 10, 14],
            [8, 18, 15, 15, 16, 19, 19, 19, 17, 14],
            [18, 18, 18, 15, 19, 19, 19, 20, 20, 14],
            [18, 18, 18, 19, 19, 19, 20, 20, 20, 14],
            [21, 18, 19, 19, 19, 20, 20, 20, 22, 23],
            [24, 24, 24, 19, 19, 20, 20, 25, 22, 23]
        ])
        self.assertEqual(expected_solution, solution)

        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_hard(self):  # approximately 350 milliseconds and 1 proposition
        grid_size = (10, 10)
        circles_positions = {
            1: Position(0, 8.5), 2: Position(0.5, 3.5), 3: Position(1, 8.5), 4: Position(2, 5), 5: Position(2.5, 0.5), 6: Position(2.5, 3),
            7: Position(3, 2), 8: Position(3, 9), 9: Position(3.5, 6.5), 10: Position(4, 1), 11: Position(5, 1), 12: Position(5, 3),
            13: Position(5, 8), 14: Position(6, 9), 15: Position(6.5, 0), 16: Position(6.5, 7.5), 17: Position(7.5, 1.5), 18: Position(7.5, 5.5),
            19: Position(8, 9), 20: Position(8.5, 3), 21: Position(8.5, 4), 22: Position(9, 0.5), 23: Position(9, 8)
        }
        game_solver = TentaiShowSolver(grid_size, circles_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
            [2, 2, 2, 2, 2, 2, 2, 2, 3, 3],
            [5, 5, 6, 6, 4, 4, 4, 9, 9, 8],
            [5, 5, 7, 6, 6, 9, 9, 9, 9, 8],
            [10, 10, 10, 12, 12, 9, 9, 9, 9, 8],
            [15, 11, 12, 12, 12, 9, 9, 13, 13, 13],
            [15, 17, 12, 12, 18, 18, 18, 16, 16, 14],
            [15, 17, 17, 18, 18, 18, 18, 16, 16, 19],
            [15, 17, 17, 20, 21, 18, 18, 18, 18, 19],
            [22, 22, 17, 20, 21, 18, 18, 18, 23, 19]
        ])
        self.assertEqual(expected_solution, solution)

        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    @unittest.skip("This test is too slow")
    def test_solution_15x15_normal(self):  # approximately 13 seconds and 14 propositions
        grid_size = (15, 15)
        circles_positions = {
            1: Position(0, 0.5), 2: Position(0, 6.5), 3: Position(0, 9), 4: Position(0, 13), 5: Position(0.5, 4.5), 6: Position(0.5, 14), 7: Position(1, 7), 8: Position(1.5, 0),
            9: Position(1.5, 9.5), 10: Position(2, 13), 11: Position(2.5, 2), 12: Position(2.5, 3), 13: Position(2.5, 4.5), 14: Position(2.5, 6.5), 15: Position(3, 0.5),
            16: Position(3, 10), 17: Position(4, 8.5), 18: Position(4.5, 4), 19: Position(5, 1), 20: Position(5, 3), 21: Position(5, 11.5), 22: Position(5.5, 0),
            23: Position(6, 6), 24: Position(6, 10), 25: Position(6, 12.5), 26: Position(7, 1.5), 27: Position(7.5, 13.5), 28: Position(8, 3), 29: Position(8, 4),
            30: Position(8, 10), 31: Position(8.5, 6.5), 32: Position(9, 9.5), 33: Position(9.5, 0), 34: Position(9.5, 11.5), 35: Position(9.5, 14), 36: Position(10, 1),
            37: Position(10, 8.5), 38: Position(11, 12), 39: Position(11.5, 1.5), 40: Position(11.5, 10), 41: Position(11.5, 13.5), 42: Position(12.5, 7), 43: Position(12.5, 11.5),
            44: Position(13, 3.5), 45: Position(13, 13), 46: Position(14, 12.5)
        }
        game_solver = TentaiShowSolver(grid_size, circles_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 11, 5, 5, 5, 2, 2, 3, 3, 3, 9, 10, 4, 6],
            [8, 11, 11, 11, 5, 5, 5, 7, 9, 9, 9, 9, 10, 10, 6],
            [8, 15, 11, 12, 13, 13, 14, 14, 9, 9, 9, 9, 10, 10, 10],
            [15, 15, 11, 12, 13, 13, 14, 14, 9, 17, 16, 17, 17, 10, 10],
            [15, 11, 11, 11, 18, 17, 17, 17, 17, 17, 17, 17, 17, 25, 10],
            [22, 19, 11, 20, 18, 17, 17, 23, 17, 23, 24, 21, 21, 25, 25],
            [22, 26, 26, 23, 23, 23, 23, 23, 23, 23, 24, 25, 25, 25, 25],
            [33, 26, 26, 23, 29, 23, 31, 31, 31, 31, 24, 25, 25, 27, 27],
            [33, 26, 26, 28, 29, 31, 31, 31, 31, 30, 30, 30, 25, 27, 27],
            [33, 39, 39, 39, 29, 31, 31, 31, 31, 32, 32, 34, 34, 41, 35],
            [33, 36, 39, 39, 31, 31, 31, 31, 37, 37, 40, 34, 34, 41, 35],
            [33, 39, 39, 42, 42, 42, 42, 42, 42, 42, 40, 40, 38, 41, 41],
            [33, 39, 39, 44, 44, 42, 42, 42, 42, 40, 40, 43, 43, 41, 41],
            [39, 39, 44, 44, 44, 44, 42, 42, 42, 42, 40, 43, 43, 45, 41],
            [39, 39, 39, 44, 44, 42, 42, 42, 42, 42, 42, 42, 46, 46, 41]
        ])
        self.assertEqual(expected_solution, solution)

    def test_solution_15x15_hard(self):  # approximately 5 seconds and 13 propositions
        grid_size = (15, 15)
        circles_positions = {
            1: Position(0, 0.5), 2: Position(0, 5), 3: Position(0, 11.5), 4: Position(0.5, 3.5), 5: Position(0.5, 9.5), 6: Position(1, 1), 7: Position(1, 5.5), 8: Position(1.5, 13.5),
            9: Position(2, 7), 10: Position(2, 10.5), 11: Position(2.5, 2), 12: Position(3, 4.5), 13: Position(3, 12), 14: Position(3.5, 10.5), 15: Position(4, 2.5),
            16: Position(4, 14), 17: Position(5, 0), 18: Position(5, 2), 19: Position(5, 4.5), 20: Position(5, 6.5), 21: Position(5, 8), 22: Position(5, 9),
            23: Position(5.5, 10.5), 24: Position(6, 1), 25: Position(6, 12), 26: Position(6.5, 3.5), 27: Position(7.5, 6.5), 28: Position(7.5, 9.5), 29: Position(7.5, 12.5),
            30: Position(8.5, 2.5), 31: Position(9, 0.5), 32: Position(9, 8), 33: Position(9, 13.5), 34: Position(11, 0.5), 35: Position(11, 10.5), 36: Position(11, 12),
            37: Position(11, 14), 38: Position(11.5, 5.5), 39: Position(11.5, 8), 40: Position(11.5, 13), 41: Position(12, 2.5), 42: Position(12, 4), 43: Position(12.5, 10),
            44: Position(13, 0), 45: Position(13, 7), 46: Position(13, 9), 47: Position(13, 13.5), 48: Position(14, 7), 49: Position(14, 11.5)
        }
        game_solver = TentaiShowSolver(grid_size, circles_positions, self.get_solver_engine())
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

    @unittest.skip("not working")
    def test_solution_20x20_2025_01_26(self):
        grid_size = (20, 20)
        circles_positions = {
            1: Position(0.0, 3.5), 2: Position(0.0, 10.0), 3: Position(0.0, 12.0), 4: Position(0.5, 6.5), 5: Position(0.5, 14.5), 6: Position(0.5, 18.5), 7: Position(1.0, 1.0), 8: Position(1.0, 4.0),
            9: Position(1.0, 17.0), 10: Position(2.0, 0.0), 11: Position(2.0, 8.0), 12: Position(2.0, 13.5), 13: Position(2.0, 16.0), 14: Position(2.5, 2.0), 15: Position(3.0, 3.0),
            16: Position(3.0, 6.0), 17: Position(3.0, 15.0), 18: Position(3.0, 19.0), 19: Position(3.5, 9.5), 20: Position(3.5, 12.5), 21: Position(3.5, 17.0), 22: Position(4.0, 18.5),
            23: Position(5.0, 3.5), 24: Position(5.0, 11.0), 25: Position(5.0, 18.5), 26: Position(5.5, 5.0), 27: Position(5.5, 6.5), 28: Position(5.5, 12.0), 29: Position(6.0, 0.0),
            30: Position(6.0, 13.0), 31: Position(6.0, 15.5), 32: Position(6.0, 18.0), 33: Position(6.5, 1.0), 34: Position(6.5, 8.0), 35: Position(7.0, 3.0), 36: Position(7.5, 5.5),
            37: Position(7.5, 7.0), 38: Position(7.5, 11.5), 39: Position(7.5, 17.5), 40: Position(8.0, 0.0), 41: Position(8.0, 4.0), 42: Position(8.0, 15.0), 43: Position(9.0, 2.5),
            44: Position(9.0, 9.0), 45: Position(9.0, 13.5), 46: Position(9.0, 17.5), 47: Position(9.5, 10.5), 48: Position(9.5, 12.0), 49: Position(10.0, 0.5), 50: Position(10.5, 4.5),
            51: Position(11.0, 2.0), 52: Position(11.0, 15.0), 53: Position(11.5, 8.0), 54: Position(11.5, 10.0), 55: Position(12.0, 1.5), 56: Position(12.5, 4.0), 57: Position(12.5, 18.5),
            58: Position(13.0, 12.0), 59: Position(13.5, 0.5), 60: Position(14.0, 3.0), 61: Position(14.0, 15.0), 62: Position(15.0, 4.5), 63: Position(15.0, 12.0), 64: Position(15.0, 16.0),
            65: Position(15.0, 19.0), 66: Position(15.5, 0.0), 67: Position(15.5, 6.5), 68: Position(15.5, 8.5), 69: Position(15.5, 10.5), 70: Position(15.5, 17.5), 71: Position(16.0, 2.0),
            72: Position(16.0, 3.0), 73: Position(16.5, 12.5), 74: Position(17.0, 11.0), 75: Position(17.5, 0.5), 76: Position(17.5, 4.0), 77: Position(17.5, 18.5), 78: Position(18.0, 15.0),
            79: Position(18.5, 2.0), 80: Position(18.5, 5.5), 81: Position(18.5, 8.0), 82: Position(18.5, 9.0), 83: Position(19.0, 0.5), 84: Position(19.0, 10.0), 85: Position(19.0, 14.0),
            86: Position(19.0, 18.0)
        }
        game_solver = TentaiShowSolver(grid_size, circles_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            []
        ])
        self.assertEqual(expected_solution, solution)

    @unittest.skip("This test is too slow")
    def test_solution_20x20_2025_01_27(self):
        grid_size = (20, 20)
        circles_positions = {
            1: Position(0.0, 0.0), 2: Position(0.0, 8.0), 3: Position(0.0, 17.0), 4: Position(0.5, 5.5), 5: Position(0.5, 7.0), 6: Position(1.0, 3.0), 7: Position(1.0, 11.5), 8: Position(1.0, 16.5),
            9: Position(1.0, 19.0), 10: Position(1.5, 0.5), 11: Position(2.0, 7.0), 12: Position(2.0, 18.0), 13: Position(3.0, 3.0), 14: Position(3.0, 10.5), 15: Position(3.0, 14.0),
            16: Position(3.5, 1.5), 17: Position(3.5, 7.5), 18: Position(3.5, 16.5), 19: Position(4.0, 9.0), 20: Position(4.0, 12.0), 21: Position(4.5, 4.0), 22: Position(4.5, 10.5),
            23: Position(4.5, 18.5), 24: Position(5.0, 3.0), 25: Position(5.0, 12.5), 26: Position(5.5, 5.5), 27: Position(6.0, 1.0), 28: Position(6.0, 15.5), 29: Position(6.0, 17.0),
            30: Position(6.5, 8.5), 31: Position(6.5, 12.5), 32: Position(6.5, 18.5), 33: Position(7.0, 2.0), 34: Position(7.0, 4.0), 35: Position(7.0, 16.5), 36: Position(8.0, 0.0),
            37: Position(8.0, 1.5), 38: Position(8.0, 3.0), 39: Position(8.0, 12.0), 40: Position(8.5, 4.5), 41: Position(8.5, 15.5), 42: Position(9.5, 9.0), 43: Position(9.5, 12.0),
            44: Position(9.5, 19.0), 45: Position(10.0, 1.5), 46: Position(10.0, 6.5), 47: Position(10.0, 11.0), 48: Position(10.5, 5.0), 49: Position(10.5, 15.5), 50: Position(10.5, 18.0),
            51: Position(11.0, 3.0), 52: Position(11.0, 8.0), 53: Position(11.0, 12.5), 54: Position(11.5, 10.5), 55: Position(12.0, 5.5), 56: Position(12.5, 7.5), 57: Position(13.0, 13.5),
            58: Position(13.5, 1.5), 59: Position(13.5, 9.5), 60: Position(13.5, 16.5), 61: Position(13.5, 18.5), 62: Position(14.0, 4.0), 63: Position(14.0, 15.0), 64: Position(14.5, 11.0),
            65: Position(15.0, 5.5), 66: Position(15.0, 9.0), 67: Position(15.5, 12.0), 68: Position(16.0, 2.5), 69: Position(16.0, 7.5), 70: Position(16.0, 16.0), 71: Position(16.5, 0.5),
            72: Position(16.5, 9.5), 73: Position(17.5, 2.0), 74: Position(18.0, 4.0), 75: Position(18.0, 13.0), 76: Position(18.0, 17.5), 77: Position(18.5, 0.5), 78: Position(18.5, 6.0),
            79: Position(18.5, 8.5), 80: Position(19.0, 2.5), 81: Position(19.0, 10.0), 82: Position(19.0, 12.5), 83: Position(19.0, 16.0)
        }
        game_solver = TentaiShowSolver(grid_size, circles_positions, self.get_solver_engine())
        solution = game_solver.get_solution()
        expected_solution = Grid([
            []
        ])
        self.assertEqual(expected_solution, solution)


if __name__ == '__main__':
    unittest.main()
