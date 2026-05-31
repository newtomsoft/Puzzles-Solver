import unittest
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Kuroshuto.KuroshutoSolver import KuroshutoSolver

_ = KuroshutoSolver.EMPTY
B = KuroshutoSolver.BLACK
W = KuroshutoSolver.WHITE


class KuroshutoSolverTests(unittest.IsolatedAsyncioTestCase):
    def test_solve_5x5_easy_3eqd2(self):
        """https://gridpuzzle.com/kuroshuto/3eqd2"""
        input_grid = Grid([
            [1, 3, 2, 4, _],
            [_, _, _, _, _],
            [4, 3, 2, 2, _],
            [2, _, _, 1, _],
            [_, 2, 3, _, 4]
        ])
        expected_solution = Grid([
            [W, W, W, W, B],
            [B, W, B, W, W],
            [W, W, W, W, B],
            [W, W, W, W, W],
            [W, W, W, B, W]
        ])

        solver = KuroshutoSolver(input_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solve_8x8_evil_015r2(self):
        """https://gridpuzzle.com/kuroshuto/015r2"""
        input_grid = Grid([
            [1, _, _, _, 2, 2, _, _],
            [_, _, _, 5, _, _, 2, 2],
            [_, _, 5, _, _, 1, 3, _],
            [2, _, _, _, _, _, _, 3],
            [3, _, _, _, _, _, _, 2],
            [_, 1, 2, _, _, 2, _, _],
            [5, 4, _, _, 3, _, _, _],
            [_, _, 2, 2, _, _, _, 1]
        ])
        expected_solution = Grid([
            [W, W, W, B, W, W, B, W],
            [B, W, W, W, W, B, W, W],
            [W, B, W, B, W, W, W, B],
            [W, W, W, W, B, W, B, W],
            [W, B, W, W, W, W, W, W],
            [W, W, W, W, B, W, W, B],
            [W, W, W, B, W, W, W, W],
            [W, B, W, W, B, W, B, W]
        ])
        solver = KuroshutoSolver(input_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solve_10x10_evil_0g268(self):
        """https://gridpuzzle.com/kuroshuto/0g268"""
        input_grid = Grid([
            [_, _, _, 7, _, 7, _, 1, 4, 2],
            [_, _, _, _, 2, _, 3, _, 4, _],
            [_, _, _, _, _, _, _, _, _, _],
            [1, 1, 5, _, _, _, 5, _, _, _],
            [_, _, _, 5, _, _, _, _, 3, _],
            [_, 2, _, _, _, 2, _, _, _, 9],
            [_, _, _, 4, _, 3, _, _, 2, _],
            [_, _, _, _, 3, _, 7, _, _, _],
            [8, _, 7, _, _, 6, _, 3, _, _],
            [_, _, _, _, 4, 5, _, _, _, 3]
        ])
        expected_solution = Grid([
            [B, W, W, W, B, W, B, W, W, W],
            [W, W, B, W, W, W, W, W, W, W],
            [B, W, W, B, W, B, W, W, W, B],
            [W, W, W, W, W, W, W, B, W, W],
            [W, B, W, W, W, W, B, W, W, W],
            [B, W, W, W, W, W, W, W, B, W],
            [W, W, B, W, W, W, B, W, W, B],
            [W, B, W, B, W, B, W, W, B, W],
            [W, W, W, W, B, W, B, W, W, W],
            [B, W, W, B, W, W, W, W, W, W]
        ])
        solver = KuroshutoSolver(input_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)

    def test_solve_15x15_evil_0edjr(self):
        """https://gridpuzzle.com/kuroshuto/0edjr"""
        input_grid = Grid([
            [_, _, _, 4, _, 5, _, 4, 5, _, 4, _, _, _, _],
            [2, 4, 1, _, _, _, _, 3, _, 6, _, _, 2, _, 8],
            [_, _, _, 3, _, 3, _, _, _, _, _, _, 4, _, 1],
            [_, _, _, _, _, _, 2, 2, 3, _, _, 1, _, _, _],
            [_, _, 1, _, 4, _, _, _, _, 4, 2, _, _, _, 3],
            [5, _, 3, _, _, _, _, _, 3, _, 3, _, _, _, _],
            [_, 1, _, 1, _, _, _, 4, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, 4, _, _, _, 6, _, _, 5, _],
            [1, 3, _, _, 3, 2, _, _, _, _, _, _, _, _, 5],
            [_, _, _, _, 3, 2, 1, 4, _, 4, _, _, 4, _, _],
            [_, _, _, _, 2, _, _, _, 9, _, _, 2, _, 1, 3],
            [1, _, _, _, _, _, _, _, 6, 1, _, 4, _, 3, _],
            [_, _, _, 1, 1, _, 8, _, 8, _, _, _, 4, _, _],
            [_, _, _, _, _, _, 7, _, _, _, _, 4, _, 9, _],
            [_, 1, 1, 6, _, _, _, _, 1, _, _, 1, _, _, 9]
        ])
        expected_solution = Grid([
            [B, W, W, W, W, W, B, W, W, W, W, B, W, B, W],
            [W, W, W, W, W, B, W, W, B, W, B, W, W, W, W],
            [W, W, B, W, W, W, B, W, W, W, W, B, W, W, W],
            [B, W, W, W, B, W, W, W, W, B, W, W, W, W, B],
            [W, W, W, B, W, W, B, W, B, W, W, W, W, B, W],
            [W, W, W, W, B, W, W, W, W, B, W, B, W, W, W],
            [W, W, B, W, W, W, B, W, B, W, W, W, B, W, W],
            [B, W, W, W, W, B, W, W, W, B, W, B, W, W, B],
            [W, W, W, W, W, W, B, W, W, W, B, W, B, W, W],
            [W, B, W, W, W, W, W, W, B, W, W, W, W, W, B],
            [W, W, B, W, W, B, W, B, W, W, W, W, B, W, W],
            [W, B, W, B, W, W, B, W, W, W, B, W, W, W, B],
            [W, W, W, W, W, B, W, W, W, W, W, B, W, B, W],
            [W, W, B, W, W, W, W, B, W, W, W, W, W, W, W],
            [B, W, W, W, W, B, W, W, W, B, W, W, B, W, W]
        ])
        solver = KuroshutoSolver(input_grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)


if __name__ == '__main__':
    unittest.main()
