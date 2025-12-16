import unittest

from Domain.Board.Grid import Grid
from Domain.Puzzles.Fillomino.FillominoSolver import FillominoSolver

_ = 0


class FillominoSolverTest(unittest.TestCase):
    def test_simple_2x2_clue(self):
        grid = Grid([
            [2, _],
            [_, _]
        ])
        solver = FillominoSolver(grid)
        solution = solver.solve()
        self.assertEqual(Grid.empty(), solution)

    def test_simple_3x3(self):
        grid = Grid([
            [_, 2, 1],
            [_, 3, 2],
            [1, _, _]
        ])
        expected_solution = Grid([
            [2, 2, 1],
            [3, 3, 2],
            [1, 3, 2]
        ])
        solver = FillominoSolver(grid)
        solution = solver.solve()
        self.assertEqual(expected_solution, solution)

    def test_simple_5x5_(self):
        grid = Grid([
            [1, _, _, 3, _],
            [9, _, 1, 7, _],
            [2, 9, 7, _, 2],
            [_, 9, 7, _, _],
            [9, _, _, 7, _],
        ])
        expected_solution = Grid([
            [1, 9, 9, 3, 3],
            [9, 9, 1, 7, 3],
            [2, 9, 7, 7, 2],
            [2, 9, 7, 7, 2],
            [9, 9, 9, 7, 7],
        ])
        solver = FillominoSolver(grid)
        solution = solver.solve()
        self.assertEqual(expected_solution, solution)

    def test_5x5_evil(self):  # 40sec
        grid = Grid([
            [4, _, 3, _, _],
            [_, _, 4, 3, _],
            [1, _, 7, _, _],
            [_, 5, 4, _, _],
            [_, _, _, _, 7],

        ])
        expected_solution = Grid([
            [4, 1, 3, 3, 7],
            [4, 4, 4, 3, 7],
            [1, 5, 7, 7, 7],
            [5, 5, 4, 4, 7],
            [5, 5, 4, 4, 7],
        ])
        solver = FillominoSolver(grid)
        solution = solver.solve()
        self.assertEqual(expected_solution, solution)

    def test_6x6_evil(self):  # 55 sec
        grid = Grid([
            [9, _, _, _, 3, _],
            [_, _, _, 2, _, 3],
            [_, 9, 9, 3, _, 2],
            [2, _, 5, 3, 3, _],
            [5, _, 7, _, _, _],
            [_, 5, _, _, _, 1],
        ])
        expected_solution = Grid([
            [9, 9, 9, 9, 3, 3],
            [9, 9, 9, 2, 2, 3],
            [2, 9, 9, 3, 1, 2],
            [2, 5, 5, 3, 3, 2],
            [5, 5, 7, 7, 7, 7],
            [1, 5, 7, 7, 7, 1],
        ])
        solver = FillominoSolver(grid)
        solution = solver.solve()
        self.assertEqual(expected_solution, solution)

    def test_7x7_evil(self):  # 2mn45
        grid = Grid([
            [5, _, _, 2, 2, _, 1],
            [_, 2, _, _, _, _, 9],
            [_, 5, _, 9, 2, _, 2],
            [_, 1, 3, _, 2, 3, _],
            [2, _, 7, 7, _, 3, _],
            [3, _, _, _, _, 3, _],
            [1, _, 2, 2, _, _, 4],
        ])
        expected_solution = Grid([
            [5, 2, 9, 2, 2, 9, 1],
            [5, 2, 9, 9, 9, 9, 9],
            [5, 5, 3, 9, 2, 9, 2],
            [5, 1, 3, 3, 2, 3, 2],
            [2, 2, 7, 7, 7, 3, 4],
            [3, 3, 7, 7, 7, 3, 4],
            [1, 3, 2, 2, 7, 4, 4]
        ])
        solver = FillominoSolver(grid)
        solution = solver.solve()
        self.assertEqual(expected_solution, solution)

    def test_8x8_evil(self):  # 13mn
        grid = Grid([
            [2, _, 8, _, 8, _, _, 8],
            [_, _, 9, 3, 3, _, 3, _],
            [9, _, _, 3, _, _, 2, _],
            [_, _, 2, _, 6, _, 6, _],
            [_, 4, _, 9, _, 2, _, _],
            [_, 3, _, _, 9, _, _, 2],
            [_, 3, _, 9, 9, 9, _, _],
            [2, _, _, 2, _, 2, _, 3],
        ])
        expected_solution = Grid([
            [2, 8, 8, 8, 8, 8, 8, 8],
            [2, 9, 9, 3, 3, 8, 3, 3],
            [9, 9, 9, 3, 6, 2, 2, 3],
            [9, 9, 2, 2, 6, 6, 6, 6],
            [9, 4, 4, 9, 2, 2, 6, 2],
            [9, 3, 4, 9, 9, 9, 9, 2],
            [2, 3, 4, 9, 9, 9, 3, 3],
            [2, 3, 2, 2, 9, 2, 2, 3]
        ])
        solver = FillominoSolver(grid)
        solution = solver.solve()
        self.assertEqual(expected_solution, solution)


if __name__ == '__main__':
    unittest.main()
