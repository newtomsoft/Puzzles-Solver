import unittest
from unittest import TestCase
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Usotatami.UsotatamiSolver import UsotatamiSolver

_ = None

class UsotatamiSolverTests(TestCase):
    def test_4x4(self):
        # https://gridpuzzle.com/usotatami/ov8dz
        grid = Grid([
            [_, _, 3, _],
            [_, _, _, 2],
            [1, _, 2, _],
            [_, _, 1, 1]
        ])

        solver = UsotatamiSolver(grid)
        solution = solver.get_solution()
        expected_solution = Grid([
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [2, 2, 3, 5],
            [4, 4, 4, 5],
        ])
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_5x5(self):
        # https://gridpuzzle.com/usotatami/lgxp4
        grid = Grid([
            [1, 4, _, _, 1],
            [_, _, _, 4, 3],
            [2, _, _, _, 2],
            [_, _, _, _, 1],
            [4, 4, 4, 3, 4]
        ])

        solver = UsotatamiSolver(grid)
        solution = solver.get_solution()
        expected_solution = Grid([
            [0, 1, 2, 2, 2],
            [0, 1, 3, 3, 4],
            [5, 1, 6, 6, 6],
            [7, 7, 7, 7, 7],
            [8, 9, 10, 11, 12]
        ])
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_6x6(self):
        # https://gridpuzzle.com/usotatami/yq1xk
        grid = Grid([
            [_, _, 2, _, 2, _],
            [_, _, 1, _, _, _],
            [5, _, _, _, _, _],
            [2, _, 1, 4, _, 4],
            [3, _, _, _, 3, 4],
            [4, 2, _, 2, 1, _]
        ])

        solver = UsotatamiSolver(grid)
        solution = solver.get_solution()
        expected_solution = Grid([
            [0, 0, 0, 1, 1, 1],
            [2, 2, 2, 2, 2, 2],
            [3, 3, 3, 3, 3, 3],
            [4, 12, 5, 6, 7, 7],
            [8, 12, 5, 9, 9, 10],
            [11, 12, 5, 13, 14, 14]
        ])
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_7x7(self):
        # https://gridpuzzle.com/usotatami/wrx2q
        grid = Grid([
            [_, _, _, _, _, _, _],
            [_, _, 2, _, 2, 2, _],
            [2, _, _, 4, _, _, _],
            [4, 4, _, 4, _, 3, _],
            [2, _, _, _, _, _, 2],
            [_, _, 4, 2, _, _, 4],
            [_, 5, _, 1, 2, 2, 2]
        ])

        solver = UsotatamiSolver(grid)
        solution = solver.get_solution()
        expected_solution = Grid([
            [3, 6, 0, 4, 1, 2, 10],
            [3, 6, 0, 4, 1, 2, 10],
            [3, 6, 0, 4, 1, 2, 10],
            [5, 6, 0, 7, 1, 8, 10],
            [9, 6, 11, 7, 16, 8, 10],
            [9, 14, 11, 12, 16, 13, 13],
            [9, 14, 15, 15, 16, 17, 18]
        ])
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_8x8(self):
        # https://gridpuzzle.com/usotatami/pn7wv
        grid = Grid([
            [_, _, _, _, 5, 4, _, _],
            [3, _, _, 4, 1, _, _, _],
            [1, _, _, 2, _, 2, _, _],
            [4, 4, 2, 2, _, _, 4, _],
            [_, _, _, _, 3, _, _, _],
            [1, 4, 3, _, _, _, _, 4],
            [_, _, _, _, 2, 3, _, 3],
            [3, 4, _, _, _, 1, 2, 4]
        ])

        solver = UsotatamiSolver(grid)
        solution = solver.get_solution()
        expected_solution = Grid([
            [2, 0, 0, 0, 0, 1, 12, 17],
            [2, 3, 3, 3, 4, 1, 12, 17],
            [5, 5, 10, 6, 4, 7, 12, 17],
            [8, 9, 10, 11, 4, 19, 12, 17],
            [8, 15, 10, 11, 13, 19, 12, 17],
            [14, 15, 16, 11, 13, 19, 24, 17],
            [14, 22, 16, 11, 18, 19, 24, 20],
            [21, 22, 23, 23, 23, 23, 24, 25]
        ])
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())

    def test_9x9(self):
        # https://gridpuzzle.com/usotatami/0xww1
        grid = Grid([
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, 4, _, _, _, _, _],
            [_, _, 4, _, _, 4, 2, 1, _],
            [_, _, _, _, 1, _, _, _, _],
            [1, 2, _, _, 1, _, 4, 4, _],
            [_, _, 2, _, _, 5, 1, _, _],
            [4, 1, 4, _, 3, _, _, _, _],
            [_, _, _, _, 1, 4, _, 2, _],
            [4, 3, 4, 6, 1, _, 4, 3, 4]
        ])

        solver = UsotatamiSolver(grid)
        solution = solver.get_solution()
        expected_solution = Grid([
            [6, 7, 1, 0, 5, 2, 3, 4, 28],
            [6, 7, 1, 0, 5, 2, 3, 4, 28],
            [6, 7, 1, 0, 5, 2, 3, 4, 28],
            [6, 7, 11, 0, 5, 12, 3, 10, 28],
            [6, 7, 11, 0, 8, 12, 9, 10, 28],
            [6, 15, 11, 0, 8, 12, 13, 13, 28],
            [14, 15, 16, 0, 17, 17, 17, 17, 28],
            [18, 18, 18, 18, 18, 19, 26, 20, 28],
            [21, 22, 23, 24, 25, 25, 26, 27, 28]
        ])
        self.assertEqual(expected_solution, solution)
        self.assertEqual(Grid.empty(), solver.get_other_solution())

if __name__ == '__main__':
    unittest.main()
