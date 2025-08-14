import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.StarsAndArrows.StarsAndArrowsSolver import StarsAndArrowsSolver

_ = 0
__ = -1
___ = ''
X = 1


class StarsAndArrowsSolverTests(TestCase):
    def test_solution_basic_rows_count(self):
        grid = Grid([
            ['↓', ___],
            [___, '↑']
        ])
        counts = {
            'left': [1, 1],
            'up': [__, __]
        }
        expected_solution = Grid([
            [_, X],
            [X, _]
        ])
        solver = StarsAndArrowsSolver(grid, counts)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_basic_columns_count(self):
        grid = Grid([
            ['↓', ___],
            [___, '↑']
        ])
        counts = {
            'left': [__, __],
            'up': [1, 1]
        }
        expected_solution = Grid([
            [_, X],
            [X, _]
        ])
        solver = StarsAndArrowsSolver(grid, counts)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_basic_arrow_up_down(self):
        grid = Grid([
            ['↓', ___],
            [___, '↑']
        ])
        counts = {
            'left': [__, __],
            'up': [__, __]
        }
        expected_solution = Grid([
            [_, X],
            [X, _]
        ])
        solver = StarsAndArrowsSolver(grid, counts)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_basic_arrow_left_right(self):
        grid = Grid([
            ['→', ___],
            [___, '←']
        ])
        counts = {
            'left': [__, __],
            'up': [__, __]
        }
        expected_solution = Grid([
            [_, X],
            [X, _]
        ])
        solver = StarsAndArrowsSolver(grid, counts)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_basic_arrow_up_left_right(self):
        grid = Grid([
            [___, ___],
            ['↗', '↖']
        ])
        counts = {
            'left': [__, __],
            'up': [__, __]
        }
        expected_solution = Grid([
            [X, X],
            [_, _]
        ])
        solver = StarsAndArrowsSolver(grid, counts)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_basic_arrow_down_left_right(self):
        grid = Grid([
            ['↘', '↙'],
            [___, ___]
        ])
        counts = {
            'left': [__, __],
            'up': [__, __]
        }
        expected_solution = Grid([
            [_, _],
            [X, X]
        ])
        solver = StarsAndArrowsSolver(grid, counts)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_basic_same_cont_arrows_stars(self):
        grid = Grid([
            [___, ___, ___, ___, ___],
            [___, ___, '↓', ___, ___],
            [___, '→', ___, '←', ___],
            [___, ___, '↑', ___, ___],
            [___, ___, ___, ___, ___],
        ])
        counts = {
            'left': [__, __],
            'up': [__, __]
        }
        expected_solution = Grid([
            [_, _, X, _, _],
            [_, _, _, _, _],
            [X, _, _, _, X],
            [_, _, _, _, _],
            [_, _, X, _, _],
        ])
        solver = StarsAndArrowsSolver(grid, counts)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_4x4_easy_31q6k(self):
        """https://gridpuzzle.com/stars-and-arrows/31q6k"""
        grid = Grid([
            [___, ___, ___, ___],
            [___, '↗', '↖', ___],
            [___, '→', ___, '↙'],
            ['↑', ___, ___, ___]
        ])
        counts = {
            'left': [2, 1, 1, 1],
            'up': [1, 1, 3, 0]
        }
        expected_solution = Grid([
            [_, X, X, _],
            [X, _, _, _],
            [_, _, X, _],
            [_, _, X, _]
        ])
        solver = StarsAndArrowsSolver(grid, counts)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_8x8_evil_2kke8(self):
        """https://gridpuzzle.com/stars-and-arrows/2kke8"""
        grid = Grid([
            [___, '↓', ___, ___, ___, ___, '←', ___],
            ['↘', ___, ___, '↓', '→', ___, '↗', '↓'],
            [___, ___, ___, ___, '↘', ___, ___, ___],
            [___, ___, ___, ___, ___, '↙', '↑', ___],
            [___, ___, ___, ___, ___, ___, ___, ___],
            [___, ___, ___, ___, ___, ___, ___, ___],
            [___, '→', ___, ___, ___, ___, ___, '↖'],
            ['↑', ___, '↑', ___, ___, ___, ___, '←'],
        ])
        counts = {
            'left': [__, 2, 2, __, __, 3, 2, __],
            'up': [__, __, __, 1, __, 1, 4, __]
        }
        expected_solution = Grid([
            [_, _, _, _, X, _, _, X],
            [_, X, _, _, _, X, _, _],
            [_, _, _, _, _, _, X, X],
            [_, _, _, X, _, _, _, _],
            [_, _, _, _, X, _, X, _],
            [_, _, X, _, X, _, X, _],
            [X, _, _, _, _, _, X, _],
            [_, _, _, _, X, _, _, _]
        ])
        solver = StarsAndArrowsSolver(grid, counts)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
