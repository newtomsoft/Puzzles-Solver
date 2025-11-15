from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Neighbours.NeighboursSolver import NeighboursSolver

_ = NeighboursSolver.empty


class NeighboursSolverTests(TestCase):
    def test_4x4_easy_31yn9(self):
        """https://gridpuzzle.com/neighbours/31yn9"""
        grid = Grid([
            [_, _, _, 2],
            [2, 3, 3, _],
            [4, _, _, 4],
            [_, 2, _, 2],
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [2, 3, 4, 1],
            [2, 3, 4, 1],
            [5, 5, 6, 6],
            [7, 7, 8, 8],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_5x5_evil_1ygx0(self):
        """https://gridpuzzle.com/neighbours/1ygx0"""
        grid = Grid([
            [2, _, _, _, _],
            [2, _, 3, _, _],
            [_, _, _, _, _],
            [_, _, _, _, _],
            [_, _, _, 2, 1],
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 3, 4, 5],
            [2, 1, 3, 4, 5],
            [2, 1, 3, 4, 5],
            [2, 1, 3, 4, 5],
            [2, 2, 3, 4, 5],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_6x6_evil_0pvkr(self):
        """https://gridpuzzle.com/neighbours/0pvkr"""
        grid = Grid([
            [3, _, _, _, _, 2],
            [_, _, _, _, _, _],
            [_, 5, 4, _, _, 5],
            [3, _, _, _, _, _],
            [_, _, _, _, _, _],
            [3, _, 3, _, 2, _],
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 1, 1, 4, 2, 2],
            [6, 3, 1, 4, 2, 2],
            [6, 3, 4, 4, 5, 5],
            [6, 3, 3, 5, 5, 9],
            [6, 7, 7, 8, 8, 9],
            [7, 7, 8, 8, 9, 9],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_8x8_hard_2kdz5(self):
        """https://gridpuzzle.com/neighbours/2kdz5"""
        grid = Grid([
            [4, _, 3, _, _, _, _, 4],
            [_, _, _, _, _, _, 3, _],
            [_, _, 6, _, 6, _, _, _],
            [_, 4, _, _, 6, _, _, _],
            [_, _, _, 4, _, _, _, _],
            [3, _, _, 6, _, _, _, _],
            [_, _, 4, _, _, 6, _, 4],
            [_, _, _, 2, _, _, _, 3],
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [1, 2, 2, 2, 2, 4, 4, 3],
            [1, 1, 1, 6, 6, 4, 4, 3],
            [7, 7, 5, 5, 6, 6, 3, 3],
            [10, 7, 5, 5, 8, 8, 8, 14],
            [10, 7, 11, 9, 9, 9, 8, 14],
            [10, 10, 11, 11, 11, 9, 13, 14],
            [12, 12, 12, 12, 13, 13, 13, 14],
            [15, 15, 15, 15, 16, 16, 16, 16],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_9x9_evil_0me88(self):
        """https://gridpuzzle.com/neighbours/0me88"""
        grid = Grid([
            [_, _, 3, _, _, 0, 3, _, _],
            [4, _, 5, _, _, _, _, _, 2],
            [_, 0, _, _, _, 0, _, _, _],
            [0, _, 5, _, _, _, _, 0, 4],
            [_, _, 5, _, _, 4, 5, _, _],
            [0, _, _, _, _, 0, _, 0, _],
            [4, _, _, 0, 5, _, 5, _, _],
            [_, _, _, _, _, _, 0, _, 3],
            [_, 0, _, 4, 3, _, _, _, _]
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [4, 1, 1, 1, 2, 2, 3, 6, 6],
            [4, 4, 5, 5, 5, 2, 3, 3, 6],
            [9, 7, 7, 7, 8, 8, 11, 11, 12],
            [9, 9, 10, 10, 14, 8, 15, 11, 12],
            [16, 13, 13, 10, 14, 14, 15, 15, 12],
            [16, 16, 13, 17, 17, 17, 18, 18, 18],
            [19, 19, 20, 20, 21, 22, 22, 22, 24],
            [25, 19, 26, 20, 21, 21, 23, 23, 24],
            [25, 25, 26, 26, 27, 27, 27, 23, 24],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_10x10_evil_1dxp0(self):
        """https://gridpuzzle.com/neighbours/1dxp0"""
        grid = Grid([
            [_, _, _, _, 4, _, _, _, _, 3],
            [_, 3, 7, _, _, _, _, _, _, _],
            [_, _, _, _, 4, _, _, 5, 3, _],
            [0, _, 7, _, _, 0, _, _, 3, _],
            [_, _, _, 0, _, _, _, 5, _, _],
            [_, 3, _, _, _, _, 0, _, _, _],
            [4, _, _, _, _, _, _, _, _, 0],
            [0, _, _, _, 4, 0, _, _, _, _],
            [0, _, _, _, 0, _, _, 4, _, _],
            [_, _, _, _, _, _, _, 5, _, 2]
        ])

        game_solver = NeighboursSolver(grid)
        solution = game_solver.get_solution()
        expected_solution = Grid([
            [3, 3, 1, 1, 1, 1, 2, 2, 2, 2],
            [3, 3, 4, 5, 5, 5, 6, 6, 7, 7],
            [8, 8, 4, 4, 5, 10, 6, 6, 7, 7],
            [8, 8, 9, 4, 10, 10, 10, 13, 11, 11],
            [14, 14, 9, 12, 12, 12, 12, 13, 13, 11],
            [14, 14, 9, 9, 20, 20, 15, 17, 13, 11],
            [16, 16, 16, 19, 19, 20, 15, 17, 17, 17],
            [18, 18, 16, 19, 19, 20, 15, 23, 23, 23],
            [21, 18, 18, 22, 22, 24, 15, 23, 25, 25],
            [21, 21, 21, 22, 22, 24, 24, 24, 25, 25],
        ])
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)
