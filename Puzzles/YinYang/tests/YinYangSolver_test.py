import unittest
from unittest import TestCase

from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine
from Utils.Grid import Grid
from YinYang.YinYangSolver import YinYangSolver


class YinYangSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_square_constraint(self):
        grid = Grid([
            [1, 1, 1, 1, 1, 1],
            [1, '', 0, 0, 0, 0],
            [1, 1, 1, '', '', 0],
            [1, '', 1, 1, 1, 0],
            [1, 0, '', '', '', 0],
            [1, 0, 0, 0, 0, 0],
        ])
        expected_grid = Grid([
            [1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 1, 0],
            [1, 0, 1, 1, 1, 0],
            [1, 0, 1, 0, 1, 0],
            [1, 0, 0, 0, 0, 0],
        ])
        game_solver = YinYangSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_square_diag(self):
        grid = Grid([
            [1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 1, ''],
            [1, 0, 1, 1, 1, ''],
            [1, 0, '', '', '', ''],
            [1, 0, '', '', '', ''],
        ])
        expected_grid = Grid([
            [1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 1, 0],
            [1, 0, 1, 1, 1, 0],
            [1, 0, 1, 0, 1, 0],
            [1, 0, 0, 0, 0, 0],
        ])
        game_solver = YinYangSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_easy(self):
        grid = Grid([
            ['', '', '', '', '', 1],
            ['', '', 0, '', 0, 0],
            ['', 1, '', '', '', ''],
            ['', '', 1, 1, '', ''],
            ['', 0, '', '', '', ''],
            [1, 0, '', '', '', ''],
        ])
        expected_grid = Grid([
            [1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 1, 0],
            [1, 0, 1, 1, 1, 0],
            [1, 0, 1, 0, 1, 0],
            [1, 0, 0, 0, 0, 0],
        ])
        game_solver = YinYangSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_normal(self):
        grid = Grid([
            ['', '', '', 1, '', 0],
            [1, '', '', '', '', ''],
            ['', 1, '', 1, '', ''],
            ['', 0, '', '', 1, ''],
            ['', 0, 0, '', 1, ''],
            ['', '', '', '', '', ''],
        ])
        expected_grid = Grid([
            [1, 1, 1, 1, 1, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0],
            [1, 0, 1, 0, 1, 0],
            [1, 0, 0, 0, 1, 0],
            [1, 1, 1, 0, 0, 0]
        ])
        game_solver = YinYangSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6_hard(self):
        grid = Grid([
            ['', '', 1, '', '', 1],
            [1, '', '', 1, '', ''],
            ['', 0, '', '', '', ''],
            ['', '', '', '', 0, ''],
            ['', '', 1, 0, 0, ''],
            ['', '', '', '', '', ''],
        ])
        expected_grid = Grid([
            [1, 1, 1, 0, 0, 1],
            [1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 1],
            [1, 1, 1, 1, 1, 1],
        ])
        game_solver = YinYangSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10_hard(self):
        grid = Grid([
            ['', '', '', '', '', 1, '', 0, '', ''],
            ['', '', 1, '', '', '', '', 0, '', ''],
            ['', '', '', 0, '', '', 0, '', '', ''],
            ['', '', 0, '', 0, '', '', '', '', ''],
            ['', '', '', 0, '', 0, 0, 1, '', ''],
            ['', '', 1, '', '', 0, '', '', '', ''],
            ['', 1, '', 1, '', 0, '', '', 0, ''],
            ['', '', '', '', '', '', '', 0, '', ''],
            ['', '', 1, '', 1, 0, '', 1, '', ''],
            ['', '', '', 1, '', '', '', '', '', ''],
        ])
        expected_grid = Grid([
            [1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 0],
            [1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        ])
        game_solver = YinYangSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15_easy(self):
        grid = Grid([
            ['', '', '', '', '', '', 0, '', 1, '', '', '', '', '', ''],
            [0, '', '', 0, '', 0, '', 1, '', '', '', '', '', '', ''],
            ['', '', 1, '', 1, '', 0, 0, 0, '', 0, '', 0, '', ''],
            ['', 0, '', '', '', 0, '', 1, '', '', '', 1, '', '', ''],
            ['', '', '', 1, '', '', 0, '', '', 1, '', '', '', 1, ''],
            ['', 0, '', '', '', 0, '', 1, '', 0, '', 0, '', '', ''],
            ['', '', '', 1, '', '', 0, 0, '', '', '', '', 0, '', ''],
            ['', '', 0, '', '', 0, '', '', 0, '', 0, '', '', '', ''],
            ['', '', 0, '', 1, 0, 1, 0, 0, 1, '', '', '', 1, ''],
            ['', 0, 1, 1, '', 0, '', '', 0, '', '', '', '', '', ''],
            ['', 0, 1, '', 0, '', 1, '', '', '', '', '', 0, '', ''],
            ['', 0, 1, 0, '', 0, 1, 0, '', '', '', 1, '', '', ''],
            ['', 0, 1, 0, 1, 0, 1, 0, 1, 0, '', '', 0, '', ''],
            ['', '', 1, '', 1, '', 1, '', 1, '', '', 1, '', '', ''],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        ])
        expected_grid = Grid([
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ])
        game_solver = YinYangSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15_hard(self):
        grid = Grid([
            [1, '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['', 1, '', '', '', '', '', '', '', '', '', '', '', '', 1],
            ['', '', '', 1, 1, 1, 1, 1, '', 1, 1, '', 1, '', ''],
            ['', 0, '', 0, '', '', '', '', 1, '', '', 1, '', 1, ''],
            ['', '', 0, '', '', 1, 1, 1, '', '', 1, '', '', 1, ''],
            ['', '', '', 0, 0, 0, 0, 0, '', '', '', 1, '', 1, ''],
            ['', '', '', '', '', '', '', 1, '', '', 0, 1, '', 1, ''],
            ['', 0, '', 0, '', 0, '', '', '', '', '', 1, '', 1, ''],
            ['', '', '', 0, '', 0, '', 0, '', 0, '', '', '', 1, ''],
            ['', '', 0, '', '', 0, '', 0, '', '', '', 1, '', 1, ''],
            ['', '', 0, '', '', 0, '', 0, '', 0, '', '', '', 1, ''],
            ['', '', '', 0, '', '', 0, '', '', '', '', 1, '', 1, ''],
            ['', 0, '', '', '', '', 1, '', '', '', 0, '', '', '', ''],
            ['', '', '', '', 1, '', '', '', '', '', 0, '', 0, '', ''],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        ])
        expected_grid = Grid([
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
            [0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
            [0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
            [0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])
        game_solver = YinYangSolver(grid, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_grid, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
