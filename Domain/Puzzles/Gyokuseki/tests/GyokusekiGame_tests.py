import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Gyokuseki.GyokusekiSolver import GyokusekiSolver

_ = 0


class GyokusekiGameTests(TestCase):
    def test_solution_4x4_(self):
        """https://sudoku.one/gyokuseki/gyokuseki-1"""
        counts = {
            'left': [1, 3, 3, 1],
            'up': [1, 3, 1, 2],
            'right': [3, 1, 1, 1],
            'down': [3, 1, 2, 1]
        }
        expected_solution = Grid([
            [2, 1, 0, 1],
            [1, 1, 2, 0],
            [1, 0, 1, 2],
            [0, 2, 0, 0]
        ])
        solver = GyokusekiSolver(counts)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_7x7_tricky(self):
        """https://sudoku.one/gyokuseki/gyokuseki-56"""
        counts = {
            'left': [6, -1, 2, 4, 5, -1, -1],
            'up': [1, 4, -1, -1, -1, 2, -1],
            'right': [-1, 6, 1, 3, -1, 3, 4],
            'down': [6, 1, 4, 4, 1, -1, 4]
        }
        expected_solution = Grid([
            [0, 1, 1, 1, 1, 1, 2],
            [2, 1, 1, 1, 1, 0, 1],
            [1, 0, 2, 0, 0, 0, 0],
            [1, 1, 1, 2, 1, 0, 1],
            [1, 0, 1, 1, 1, 2, 0],
            [1, 0, 0, 1, 2, 1, 1],
            [1, 2, 1, 1, 0, 1, 0]
        ])
        solver = GyokusekiSolver(counts)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_evil(self):
        """https://gridpuzzle.com/gyokuseki/0m0d1"""
        counts = {
            'left': [7, -1, 7, -1, 3, 2, 3, 4],
            'up': [2, -1, -1, 5, 5, 4, -1, 1],
            'right': [-1, 3, 1, 7, 2, 4, 5, -1],
            'down': [5, 6, 2, 2, 3, -1, 6, 6, ]
        }
        expected_solution = Grid([
            [1, 1, 1, 1, 1, 1, 2, 0],
            [0, 2, 0, 1, 1, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 2, 0, 0, 1],
            [1, 0, 0, 2, 1, 0, 1, 1],
            [1, 1, 2, 1, 1, 0, 1, 1],
            [1, 1, 1, 0, 0, 2, 1, 1]
        ])
        solver = GyokusekiSolver(counts)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
