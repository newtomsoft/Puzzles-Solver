import unittest
from PuzzleSolver.Puzzles.Nuribou.NuribouSolver import NuribouSolver
from PuzzleSolver.Board.Grid import Grid

_ = NuribouSolver.cell_empty
X = NuribouSolver.BLACK

class TestNuribouSolver(unittest.TestCase):
    def test_solve_standard_4x4_grid(self):
        grid = Grid([
            [1, _, _, _],
            [_, 4, _, _],
            [_, _, _, 5],
            [_, _, _, _],
        ])
        expected_solution = Grid([
            [_, X, _, _],
            [X, _, X, _],
            [X, _, X, _],
            [_, _, X, _]
        ])
        
        solver = NuribouSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solve_6x6_grid(self):
        """https://gridpuzzle.com/nuribou/1n59d"""
        grid = Grid([
            [_, _, _, 5, _, 1],
            [_, _, _, _, 3, _],
            [_, _, _, _, _, _],
            [_, _, _, _, _, _],
            [8, _, _, _, _, _],
            [_, _, _, 2, _, 2]
        ])
        expected_solution = Grid([
            [_, X, _, _, X, _],
            [_, X, _, X, _, X],
            [_, X, _, X, _, X],
            [_, X, _, X, _, X],
            [_, _, X, _, X, _],
            [_, _, X, _, X, _]
        ])

        solver = NuribouSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solve_8x8_grid(self):
        """https://gridpuzzle.com/nuribou/21zq8"""
        grid = Grid([
            [_, _, _, _, 1, _, _, _],
            [_, 6, _, _, _, _, 4, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, 12, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [2, _, _, _, 8, _, _, 3],
            [_, _, 1, _, _, _, _, _]
        ])
        expected_solution = Grid([
            [_, _, X, X, _, X, X, _],
            [_, _, _, _, X, _, _, _],
            [X, X, X, X, _, X, X, X],
            [_, _, _, _, _, _, _, _],
            [_, _, X, X, X, X, _, X],
            [X, X, _, _, _, _, X, _],
            [_, _, X, _, _, _, X, _],
            [X, X, _, X, X, _, X, _]
        ])

        solver = NuribouSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solve_10x10_grid(self):
        """https://gridpuzzle.com/nuribou/29r48"""
        grid = Grid([
            [_, 3, _, _, _, _, _, _, _, 2],
            [_, _, _, _, 13, _, _, _, _, _],
            [_, _, 3, _, _, _, _, _, _, _],
            [_, _, _, _, 9, _, _, _, _, 1],
            [10, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, 4, _, _],
            [4, _, _, _, _, _, _, _, _, 4],
            [_, _, _, _, _, 8, _, _, _, _]
        ])
        expected_solution = Grid([
            [_, _, _, X, _, _, _, _, X, _],
            [X, X, X, _, _, _, _, _, X, _],
            [_, _, _, X, X, _, _, _, _, X],
            [X, X, X, _, _, X, X, X, X, _],
            [_, _, _, X, _, _, _, _, _, X],
            [X, _, _, _, X, X, _, X, _, X],
            [_, X, _, X, _, _, X, _, X, _],
            [_, X, _, X, _, _, X, _, X, _],
            [_, X, _, X, _, _, X, _, X, _],
            [_, X, _, X, _, _, X, _, X, _]
        ])

        solver = NuribouSolver(grid)
        solution = solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())


if __name__ == "__main__":
    unittest.main()
