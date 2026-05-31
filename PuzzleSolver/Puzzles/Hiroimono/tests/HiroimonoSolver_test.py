import unittest
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Hiroimono.HiroimonoSolver import HiroimonoSolver

_ = None
X = 'S'
A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T = 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29

class HiroimonoSolverTest(unittest.TestCase):
    def test_no_solution(self):
        grid = Grid([
            [X, _, X],
            [_, X, _],
            [X, _, X]
        ])
        solver = HiroimonoSolver(grid)
        solution = solver.get_solution()
        self.assertTrue(solution.is_empty())

    def test_5x5_31np0(self):
        """https://gridpuzzle.com/hiroimono/31np0"""
        grid = Grid([
            [_, _, _, _, X],
            [_, X, _, X, _],
            [_, X, _, X, X],
            [X, _, _, X, _],
            [_, _, _, X, X]
        ])
        expected_grid = Grid([
            [_, _, _, _, A],
            [_, 5, _, 6, _],
            [_, 4, _, 3, 9],
            [1, _, _, 2, _],
            [_, _, _, 7, 8]
        ])
        solver = HiroimonoSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(solution, expected_grid)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_6x6_31dp6(self):
        """https://gridpuzzle.com/hiroimono/31dp6"""
        grid = Grid([
            [_, _, _, _, X, _],
            [_, _, _, _, _, _],
            [_, X, _, X, X, _],
            [_, _, _, _, X, X],
            [_, _, _, _, X, X],
            [X, X, _, _, _, _]
        ])
        expected_grid = Grid([
            [_, _, _, _, A, _],
            [_, _, _, _, _, _],
            [_, 3, _, 4, 5, _],
            [_, _, _, _, 6, 7],
            [_, _, _, _, 9, 8],
            [1, 2, _, _, _, _]
        ])
        solver = HiroimonoSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(solution, expected_grid)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_7x7_37d49(self):
        """https://gridpuzzle.com/hiroimono/37d49"""
        grid = Grid([
            [_, _, X, _, _, X, _],
            [_, _, _, X, X, _, _],
            [_, _, _, X, X, X, X],
            [_, _, X, _, _, X, _],
            [_, _, _, _, _, _, _],
            [_, X, _, _, X, X, _],
            [X, _, _, _, X, _, X]
        ])
        expected_grid = Grid([
            [_, _, 6, _, _, 7, _],
            [_, _, _, B, A, _, _],
            [_, _, _, C, 9, 8, D],
            [_, _, 5, _, _, 4, _],
            [_, _, _, _, _, _, _],
            [_, 1, _, _, 2, 3, _],
            [G, _, _, _, F, _, E]
        ])
        solver = HiroimonoSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(solution, expected_grid)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_10x10_0xjk2(self):
        """https://gridpuzzle.com/hiroimono/0xjk2"""
        grid = Grid([
            [X, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [X, _, _, _, _, _, _, _, _, X],
            [_, X, X, X, X, X, _, _, X, _],
            [_, _, _, X, _, _, _, _, X, _],
            [_, _, X, X, _, _, _, _, _, X],
            [_, X, _, _, _, _, _, _, _, X],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, X]
        ])
        expected_grid = Grid([
            [1, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [2, _, _, _, _, _, _, _, _, 3],
            [_, E, 7, 8, D, C, _, _, B, _],
            [_, _, _, 9, _, _, _, _, A, _],
            [_, _, 6, 5, _, _, _, _, _, 4],
            [_, F, _, _, _, _, _, _, _, G],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, H]
        ])
        solver = HiroimonoSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(solution, expected_grid)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_12x12_21eqz(self):
        """https://gridpuzzle.com/hiroimono/21eqz"""
        grid = Grid([
            [X, _, _, _, _, _, _, _, _, _, X, X],
            [_, _, _, _, _, _, _, _, X, X, X, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, X, _, _, _, _, _, X, _, X, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [X, _, _, _, _, _, _, _, _, _, X, _],
            [X, X, _, _, _, _, _, _, _, _, _, _],
            [_, X, _, _, _, _, _, X, _, _, _, _],
            [X, _, _, _, _, X, _, X, _, _, _, _]
        ])
        expected_grid = Grid([
            [G, _, _, _, _, _, _, _, _, _, H, I],
            [_, _, _, _, _, _, _, _, 3, 4, 5, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, 1, _, _, _, _, _, 2, _, 6, _],
            [_, _, _, _, _, _, _, _, _, _, _, _],
            [8, _, _, _, _, _, _, _, _, _, 7, _],
            [9, A, _, _, _, _, _, _, _, _, _, _],
            [_, B, _, _, _, _, _, C, _, _, _, _],
            [F, _, _, _, _, E, _, D, _, _, _, _]
        ])
        solver = HiroimonoSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(solution, expected_grid)
        self.assertTrue(solver.get_other_solution().is_empty())

    def test_15x15_16n76(self):
        """https://gridpuzzle.com/hiroimono/16n76"""
        grid = Grid([
            [X, _, _, _, X, _, _, _, X, _, _, _, _, _, X],
            [X, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, X, _, _, X, _, _, _, _, _, _, _],
            [X, X, _, _, _, X, _, _, _, _, _, _, _, _, _],
            [_, _, X, X, _, _, _, X, _, _, _, _, _, _, X],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, X, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, X],
            [X, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [X, X, X, X, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, X, X, X, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, X, _, X, _, _, _, _, _, _, X],
            [_, _, _, _, _, _, _, X, _, _, _, X, _, _, _]
        ])
        expected_grid = Grid([
            [N, _, _, _, O, _, _, _, 4, _, _, _, _, _, 5],
            [M, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, P, _, _, Q, _, _, _, _, _, _, _],
            [L, C, _, _, _, B, _, _, _, _, _, _, _, _, _],
            [_, _, F, G, _, _, _, R, _, _, _, _, _, _, 6],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, H, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, 7],
            [K, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [J, D, E, I, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, 3, 2, 1, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, A, _, 9, _, _, _, _, _, _, 8],
            [_, _, _, _, _, _, _, S, _, _, _, T, _, _, _]
        ])
        solver = HiroimonoSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(solution, expected_grid)
        self.assertTrue(solver.get_other_solution().is_empty())


if __name__ == '__main__':
    unittest.main()
