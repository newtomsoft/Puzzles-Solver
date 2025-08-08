import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Gappy.GappySolver import GappySolver

_ = 0
X = 1


class GappySolverTests(TestCase):
    def test_solution_9x9_easy_37w1o(self):
        """https://gridpuzzle.com/gappy/37w1o"""
        rows_gaps = [3, 3, 1, 1, 7, 1, 5, 1, 5]
        columns_gaps = [2, 1, 2, 1, 1, 1, 1, 1, 1]
        expected_grid = Grid([
            [_, _, X, _, _, _, X, _, _],
            [X, _, _, _, X, _, _, _, _],
            [_, _, _, _, _, _, X, _, X],
            [_, _, X, _, X, _, _, _, _],
            [X, _, _, _, _, _, _, _, X],
            [_, _, _, X, _, X, _, _, _],
            [_, X, _, _, _, _, _, X, _],
            [_, _, _, X, _, X, _, _, _],
            [_, X, _, _, _, _, _, X, _]
        ])
        game_solver = GappySolver(rows_gaps, columns_gaps)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_18x18_evil_0jrv8(self):
        """https://gridpuzzle.com/gappy/0jrv8"""
        rows_gaps = [-1, -1, 11, 6, 1, 1, 7, 11, -1, 1, 1, -1, 1, -1, 3, 16, 1, -1]
        columns_gaps = [2, 6, -1, -1, -1, -1, 2, 4, 9, 2, 14, -1, -1, -1, 7, 4, 1, -1, ]
        expected_grid = Grid([
           [_, X, _, _, _, _, _, _, _, _, _, _, _, _, _, _, X, _],
           [_, _, _, _, _, _, _, _, X, _, X, _, _, _, _, _, _, _],
           [_, _, _, _, X, _, _, _, _, _, _, _, _, _, _, _, X, _],
           [_, _, _, _, _, _, _, X, _, _, _, _, _, _, X, _, _, _],
           [_, _, _, X, _, X, _, _, _, _, _, _, _, _, _, _, _, _],
           [_, _, _, _, _, _, _, _, _, _, _, X, _, X, _, _, _, _],
           [_, _, _, _, _, _, _, _, _, X, _, _, _, _, _, _, _, X],
           [_, X, _, _, _, _, _, _, _, _, _, _, _, X, _, _, _, _],
           [_, _, _, _, _, _, _, X, _, _, _, _, _, _, _, X, _, _],
           [_, _, _, _, _, _, _, _, _, X, _, X, _, _, _, _, _, _],
           [_, _, _, X, _, X, _, _, _, _, _, _, _, _, _, _, _, _],
           [_, _, _, _, _, _, _, _, X, _, _, _, _, _, X, _, _, _],
           [X, _, X, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
           [_, _, _, _, _, _, _, _, _, _, _, _, X, _, _, X, _, _],
           [_, _, X, _, _, _, X, _, _, _, _, _, _, _, _, _, _, _],
           [X, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, X],
           [_, _, _, _, _, _, _, _, _, _, X, _, X, _, _, _, _, _],
           [_, _, _, _, X, _, X, _, _, _, _, _, _, _, _, _, _, _]
        ])
        game_solver = GappySolver(rows_gaps, columns_gaps)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
