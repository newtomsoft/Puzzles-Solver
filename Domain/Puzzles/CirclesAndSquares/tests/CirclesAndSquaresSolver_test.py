import unittest

from playwright.sync_api import expect

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.CirclesAndSquares.CirclesAndSquaresSolver import CirclesAndSquaresSolver

B = CirclesAndSquaresSolver.Black
W = CirclesAndSquaresSolver.White
_ = CirclesAndSquaresSolver.Empty

class CirclesAndSquaresSolverTests(unittest.TestCase):
    def test_solve_5x5_easy_3n2qr(self):
        """https://gridpuzzle.com/circles-and-squares/3n2qr"""
        grid = Grid([
            [W, B, _, B, W],
            [_, _, _, _, _],
            [W, W, _, B, _],
            [W, W, _, _, B],
            [W, _, W, _, W]
        ])
        expected_solution = Grid([
            [W, B, W, B, W],
            [B, B, B, B, B],
            [W, W, W, B, W],
            [W, W, W, B, B],
            [W, W, W, B, W]
        ])

        solver = CirclesAndSquaresSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solve_5x5_hard_lznqe(self):
        """https://gridpuzzle.com/circles-and-squares/lznqe"""
        grid = Grid([
            [B, _, _, _, B],
            [_, B, _, B, _],
            [_, _, _, _, _],
            [B, _, _, _, W],
            [W, _, W, _, W]
        ])
        expected_solution = Grid([
            [B, W, B, W, B],
            [B, B, B, B, B],
            [W, B, W, W, W],
            [B, B, W, W, W],
            [W, B, W, W, W]
        ])

        solver = CirclesAndSquaresSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solve_lm88w_5x5_evil(self):
        """Test solving https://gridpuzzle.com/circles-and-squares/lm88w"""
        grid = Grid([
            [W, _, _, _, B],
            [_, W, _, B, _],
            [B, _, W, _, B],
            [B, _, _, _, W],
            [_, _, _, _, _]
        ])
        expected_solution = Grid([
            [W, B, B, B, B],
            [B, W, W, B, W],
            [B, W, W, B, B],
            [B, B, B, B, W],
            [W, B, W, B, B]
        ])

        solver = CirclesAndSquaresSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solve_7rr5j_7x7_evil(self):
        """Test solving https://gridpuzzle.com/circles-and-squares/7rr5j"""
        grid = Grid([
            [_, _, _, _, _, _, _],
            [_, W, W, _, W, B, _],
            [_, _, B, _, B, _, _],
            [B, _, _, B, _, _, W],
            [_, _, _, _, _, _, _],
            [W, _, W, _, B, _, W],
            [_, _, _, _, _, _, _]
        ])
        expected_solution = Grid([
            [B, W, W, B, B, B, B],
            [B, W, W, B, W, B, W],
            [B, B, B, W, B, B, B],
            [B, W, B, B, W, B, W],
            [B, B, W, W, B, B, B],
            [W, B, W, W, B, W, W],
            [B, B, B, B, B, W, W]
        ])

        solver = CirclesAndSquaresSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solve_p68nv_9x9_evil(self):
        """Test solving https://gridpuzzle.com/circles-and-squares/p68nv"""
        grid = Grid([
            [B, _, _, _, _, _, _, _, B],
            [_, W, _, W, _, W, _, W, _],
            [_, _, W, _, _, _, W, _, _],
            [_, B, _, _, _, _, _, B, _],
            [_, _, _, W, _, W, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [W, _, _, _, _, _, _, _, W],
            [_, _, W, _, _, _, W, _, _],
            [B, B, _, _, _, _, _, B, B]
        ])
        expected_solution = Grid([
            [B, W, W, W, B, W, W, W, B],
            [B, W, W, W, B, W, W, W, B],
            [B, W, W, W, B, W, W, W, B],
            [B, B, B, B, B, B, B, B, B],
            [W, W, W, W, B, W, W, W, W],
            [W, W, W, W, B, W, W, W, W],
            [W, W, W, W, B, W, W, W, W],
            [W, W, W, W, B, W, W, W, W],
            [B, B, B, B, B, B, B, B, B]
        ])

        solver = CirclesAndSquaresSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solve_5zrn8_12x12_evil(self):
        """Test solving https://gridpuzzle.com/circles-and-squares/5zrn8"""
        grid = Grid([
            [_, W, _, _, B, _, _, W, _, _, W, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, W, _, _, _, _, _, _, W, _, _],
            [B, _, W, _, W, _, _, W, _, W, _, W],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [B, _, B, _, _, _, _, _, _, W, _, B],
            [_, W, _, B, _, _, _, _, W, _, W, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [B, _, _, _, _, _, _, _, _, _, _, B],
            [_, W, _, _, _, W, W, _, _, _, W, _]
        ])
        expected_solution = Grid([
            [W, W, B, W, B, W, B, W, W, W, W, W],
            [W, W, B, B, B, B, B, W, W, W, W, W],
            [B, B, W, W, W, W, B, W, W, W, W, W],
            [W, B, W, W, W, W, B, W, W, W, W, W],
            [B, B, W, W, W, W, B, W, W, W, W, W],
            [W, B, W, W, W, W, B, B, B, B, B, B],
            [B, B, B, B, B, B, B, W, W, W, W, B],
            [W, W, W, B, W, W, B, W, W, W, W, B],
            [W, W, W, B, W, W, B, W, W, W, W, B],
            [W, W, W, B, B, B, B, W, W, W, W, B],
            [B, B, B, W, B, W, W, B, B, B, B, B],
            [B, W, B, B, B, W, W, B, W, B, W, B]
        ])

        solver = CirclesAndSquaresSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
