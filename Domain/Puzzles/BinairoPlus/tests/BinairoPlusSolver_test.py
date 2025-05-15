import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.BinairoPlus.BinairoPlusSolver import BinairoPlusSolver


class BinairoPlusSolverTests(TestCase):


    def test_solution_6x6(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, 1, 0, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, 0],
            [1, -1, 1, 0, -1, 1],
        ])
        comparisons_positions = {
            'equal': [
                (Position(2, 0), Position(3, 0)),
                (Position(3, 4), Position(4, 4)),
                (Position(1, 1), Position(1, 2)),
                (Position(1, 3), Position(1, 4)),
            ],
            'non_equal': [
                (Position(0, 2), Position(1, 2)),
                (Position(0, 3), Position(1, 3)),
                (Position(2, 5), Position(3, 5)),
                (Position(3, 1), Position(4, 1)),
            ],
        }
        expected_grid = Grid([
            [0, 1, 1, 0, 0, 1],
            [1, 0, 0, 1, 1, 0],
            [0, 1, 1, 0, 0, 1],
            [0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 1, 0],
            [1, 0, 1, 0, 0, 1]
        ])
        game_solver = BinairoPlusSolver(grid, comparisons_positions)
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)


if __name__ == '__main__':
    unittest.main()
