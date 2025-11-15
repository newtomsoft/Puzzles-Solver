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
