import unittest

from Domain.Board.Grid import Grid
from Domain.Puzzles.Slant.SlantSolver import SlantSolver


class SlantSolverTests(unittest.TestCase):
    def test_solve_simple(self):
        grid_clues = Grid([
            [1, None],
            [None, 1]
        ])

        expected_solution_str = '╲\n'

        solver = SlantSolver(grid_clues)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_5x5_easy_829484(self):
        grid_clues = Grid([
            [1, 1, 1, None, 2, None],
            [None, None, 2, 2, None, None],
            [None, 2, 2, None, None, 1],
            [0, 3, 2, 3, None, 1],
            [None, None, None, None, 1, None],
            [None, 1, 2, None, None, None],
        ])

        expected_solution_str = (
            '╲╲╲╱╲\n'
            '╲╲╲╱╲\n'
            '╲╲╲╱╲\n'
            '╱╲╲╲╲\n'
            '╲╲╱╲╱\n'
        )

        solver = SlantSolver(grid_clues)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_7x7_normal_5604268(self):
        grid_clues = Grid([
            [None, None, 1, 1, None, None, None, None],
            [1, 2, 2, 2, 3, 2, None, 1],
            [None, 3, None, None, 3, None, 2, None],
            [1, None, 2, None, None, None, 2, 1],
            [None, None, None, 2, 2, 2, None, 1],
            [None, 2, None, 1, None, 2, 1, 1],
            [None, 3, 2, None, 2, None, 2, None],
            [None, 1, None, None, None, None, None, None],
        ])

        expected_solution_str = (
            '╲╲╲╲╱╱╲\n'
            '╲╲╲╲╲╲╲\n'
            '╱╲╲╱╲╱╱\n'
            '╱╱╱╱╱╱╱\n'
            '╲╱╱╱╱╱╱\n'
            '╲╱╲╱╲╲╱\n'
            '╱╱╲╱╲╲╱\n'
        )

        solver = SlantSolver(grid_clues)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_10x10_normal(self):
        grid_clues = Grid([
            [None, None, None, None, 1, 1, 1, None, 1, None, None],
            [None, 3, 1, 2, None, 2, None, 3, None, 1, None],
            [1, None, 1, None, None, 2, None, 1, 3, None, None],
            [None, 3, None, None, 3, 2, 2, None, 2, None, 1],
            [None, 2, 2, 3, None, None, None, None, None, 1, None],
            [None, None, None, None, 3, None, 2, None, 1, 2, None],
            [None, None, 2, None, None, 1, 2, None, 3, None, 1],
            [None, 2, 1, None, 3, None, 3, None, 3, None, None],
            [None, 2, 2, None, None, None, 2, 3, None, 1, None],
            [1, None, 2, 1, None, 2, None, 2, 1, None, None],
            [None, 1, None, None, None, None, 1, None, 1, 1, None]
        ])

        expected_solution_str = (
            '╲╱╲╱╱╱╱╱╱╲\n'
            '╲╲╲╱╱╱╱╲╱╱\n'
            '╲╲╱╲╱╱╱╱╱╲\n'
            '╱╲╱╱╱╱╱╱╱╲\n'
            '╱╲╱╲╱╲╱╲╲╲\n'
            '╱╱╱╱╱╲╱╲╱╱\n'
            '╲╲╲╲╲╲╱╱╱╱\n'
            '╲╲╱╱╲╲╲╱╲╲\n'
            '╲╲╱╲╲╱╱╱╲╱\n'
            '╲╲╱╱╲╱╱╱╱╱\n'
        )

        solver = SlantSolver(grid_clues)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_20x20_normal(self):
        grid_clues = Grid([
            [None, None, None, 1, None, 1, None, None, 1, None, 1, None, None, None, None, None, None, None, 1, 1, None],
            [None, 3, 2, None, 1, None, 1, None, None, 2, None, None, 3, 1, None, 1, 1, 3, None, None, 1],
            [None, None, 2, None, None, None, None, None, 3, 1, 1, None, 1, 3, None, None, 2, None, None, 1, None],
            [None, 1, 1, None, None, 3, 1, 1, None, 2, None, 3, None, None, 2, 3, 1, 3, None, None, 1],
            [1, 3, None, None, 3, None, None, 2, None, 2, 3, 2, None, None, 2, 2, 2, None, 1, None, None],
            [None, None, 3, 3, None, None, None, None, None, None, None, 2, 1, None, 2, None, 2, None, 3, 1, None],
            [None, 3, None, None, 1, None, 2, None, 2, None, 2, None, None, None, None, 1, None, None, None, None, 1],
            [1, None, None, 2, 2, None, 2, None, 1, 2, 1, None, 3, None, 2, None, 3, 3, None, 2, None],
            [None, 1, 2, None, None, 2, None, None, 2, 3, None, 2, None, 1, None, None, None, None, None, 1, 1],
            [1, 3, 1, None, 2, None, 1, None, None, 2, 3, 1, None, None, 2, None, 3, 3, None, 1, None],
            [1, None, 1, None, 1, 3, 2, 1, None, None, 2, 2, None, None, 3, None, 1, 2, None, None, None],
            [None, 1, None, 2, None, None, 2, None, 1, 2, None, 1, None, 1, None, None, 3, 2, 2, None, 1],
            [None, 3, 2, None, 3, 1, 1, 3, 1, None, None, None, 2, None, 2, 1, None, 2, 1, 2, None],
            [None, None, None, None, None, 1, 3, None, None, None, 1, 2, None, None, 2, None, None, 2, None, 1, None],
            [None, 1, 1, None, None, 3, 1, None, None, 1, 1, None, 2, None, 1, 2, 3, None, 1, None, 1],
            [1, None, 2, 1, None, 1, None, None, 2, None, None, 1, None, 3, None, 2, None, 3, 1, None, 1],
            [1, None, None, None, 2, None, None, 3, None, None, 3, None, 2, None, None, None, 3, 1, 3, 1, None],
            [1, 3, None, 2, 3, 2, 1, None, None, None, None, 1, 3, 2, None, None, None, None, None, None, None],
            [1, None, 2, 3, 2, None, 2, 2, None, 1, 3, 1, 2, None, None, 2, None, None, None, 2, None],
            [None, 2, None, 1, None, 3, 3, 1, None, 1, 2, None, 2, 1, 2, 2, None, 3, 3, None, 1],
            [None, None, None, None, None, 1, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, None]
        ])

        expected_solution_str = (
            '╲╱╲╲╲╲╲╱╱╲╲╱╱╲╱╱╲╱╱╱\n'
            '╱╱╲╲╱╲╱╲╱╲╲╱╲╲╲╱╱╱╱╱\n'
            '╱╱╲╲╱╱╲╲╲╲╱╱╱╲╲╲╲╱╲╱\n'
            '╲╱╱╱╱╲╲╱╲╲╱╲╱╱╱╲╱╱╲╱\n'
            '╲╲╲╱╲╲╲╱╱╱╱╲╲╱╱╲╱╱╱╲\n'
            '╱╱╲╲╲╱╲╱╲╱╱╲╱╱╱╲╱╱╲╲\n'
            '╱╲╲╲╱╱╲╱╲╲╲╲╱╲╲╲╲╱╱╲\n'
            '╱╱╲╲╱╱╲╲╲╲╱╲╲╲╲╱╲╲╱╲\n'
            '╲╱╲╱╱╱╲╱╱╲╱╲╲╱╱╲╲╱╲╲\n'
            '╲╲╲╲╲╱╱╲╱╲╲╲╱╱╱╱╲╲╲╱\n'
            '╲╲╱╲╱╱╱╱╲╲╲╲╱╱╲╱╱╱╱╲\n'
            '╲╱╱╲╱╲╲╲╲╲╲╱╲╱╱╱╲╲╲╲\n'
            '╲╲╲╲╲╲╱╲╱╱╲╱╲╲╲╱╲╲╱╱\n'
            '╱╱╲╲╲╱╱╲╱╲╲╱╱╱╱╱╱╱╲╱\n'
            '╲╱╱╲╲╲╱╱╲╲╱╲╲╲╱╱╲╲╲╱\n'
            '╲╲╲╲╲╱╲╱╲╲╱╱╱╲╱╱╱╲╱╱\n'
            '╲╱╲╱╱╱╲╲╲╱╱╲╲╲╱╱╲╲╲╱\n'
            '╲╲╲╱╲╲╲╲╱╲╱╱╲╲╲╲╲╱╱╲\n'
            '╲╱╱╱╲╱╱╱╲╲╲╱╲╲╲╲╲╲╱╲\n'
            '╲╱╲╱╱╱╲╱╲╱╱╱╲╱╱╱╱╲╲╲\n'
        )

        solver = SlantSolver(grid_clues)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_30x30_2025_12_10(self):
        grid_clues = Grid([
            [None, None, None, 1, None, 1, None, None, None, None, 1, 1, None, None, 1, None, None, None, None, None, None, 1, None, 1, 1, 1, None, None, None, None, None],
            [None, 2, 3, None, None, 3, None, 3, None, 2, 1, None, None, 3, 2, 2, 1, None, 1, 2, None, None, 2, None, None, None, 1, 3, None, 1, None],
            [None, 3, None, None, 2, None, None, 2, None, None, None, 2, 2, None, None, 1, None, None, None, 1, 2, 1, 2, None, 1, 1, 2, None, 2, 1, None],
            [None, 2, None, 3, 2, 2, 3, None, None, 2, None, None, 3, None, 3, None, 3, None, None, 2, None, 2, None, None, None, 3, None, None, 2, None, None],
            [None, None, 2, 1, None, None, None, 3, None, 2, None, None, None, 2, 3, 3, None, 1, 2, 2, 2, 3, 2, None, 1, None, 3, None, 1, 1, None],
            [None, 3, None, None, 2, 2, 2, None, 2, None, 1, 2, None, None, None, 3, None, 2, 2, 2, 2, None, 2, None, None, 1, 1, None, None, 2, None],
            [None, 3, None, 1, 2, None, 1, 2, 2, None, None, 2, 1, None, None, None, None, None, None, 2, 1, None, 3, 3, None, None, None, None, 2, None, None],
            [None, None, None, None, None, None, None, 3, 1, None, None, 1, 3, None, None, 2, 1, None, 3, None, None, None, None, 2, None, 2, 1, None, 1, 3, None],
            [None, None, None, 3, 2, 1, 2, None, 2, None, None, 2, 1, 2, 1, None, 3, None, None, 1, None, 2, 1, 2, None, None, 1, 2, 1, 2, None],
            [None, 3, 2, None, None, 3, 1, None, None, None, None, 2, None, None, 1, None, 1, 1, None, None, None, None, None, None, 3, None, None, None, 3, None, None],
            [1, 1, 3, None, 1, 2, 1, None, None, None, 1, None, 3, None, 2, 2, None, 2, None, None, None, 1, 2, 2, None, 2, 3, 1, None, 2, None],
            [None, 1, None, 3, None, None, None, 1, None, 2, 2, None, None, 2, None, None, 2, 2, 2, 1, None, 3, 3, None, None, 2, 2, None, None, 1, None],
            [None, None, None, 1, None, 1, 3, None, 3, None, None, 3, 1, None, 3, 2, None, None, 2, 1, None, 3, None, 1, 2, None, None, 2, 2, 2, None],
            [None, 1, None, None, 1, None, None, 2, None, 1, 3, 3, 2, None, 3, None, 2, None, None, None, None, 2, None, None, None, 2, None, 2, 1, None, None],
            [None, 2, 3, None, 2, 2, None, None, None, 1, None, None, None, None, None, None, None, None, None, 3, None, None, 1, None, 3, 2, 2, 1, None, 2, None],
            [None, None, None, 1, None, 1, None, 1, None, None, 2, 2, 1, 3, 1, None, 3, None, None, None, 3, None, 2, None, 1, 2, None, None, 2, 1, None],
            [None, None, 3, None, None, 2, 2, 1, 3, 3, None, None, 2, None, 1, 2, 3, None, None, 1, 2, 3, None, 2, None, None, None, 2, 2, None, 1],
            [None, 3, 2, 3, 2, None, None, None, 2, 1, None, None, 2, None, None, 2, None, None, 1, None, None, 2, 3, None, 1, None, 3, None, None, None, None],
            [None, None, None, 2, None, 2, None, None, 2, None, 1, 3, None, 3, None, None, 3, 2, 2, 1, None, None, 2, None, None, 2, 3, 2, None, 1, 1],
            [1, 2, None, 2, 1, 2, None, 1, 1, None, None, 3, None, None, None, None, None, None, None, 1, 2, 2, None, 1, 3, 2, None, 3, None, 1, None],
            [None, 1, 2, None, 1, None, None, None, None, 1, None, None, None, None, 2, 3, None, None, 1, 2, None, 2, 1, 2, None, None, None, 3, None, None, None],
            [1, None, None, None, None, 2, None, None, 3, 2, 3, 1, 2, 2, None, None, None, None, None, 2, None, None, None, 1, 2, None, 1, None, None, 1, None],
            [1, None, 3, None, None, None, 3, None, 1, None, 3, 2, 1, 3, 2, None, None, 2, None, 2, None, 2, None, None, None, 1, None, 1, 1, 2, None],
            [None, 3, None, None, 1, None, None, 1, None, 3, 1, None, None, None, 3, None, 2, 2, None, 2, 2, None, None, None, 1, None, None, 1, None, 1, None],
            [1, None, 3, None, 1, 1, 3, None, 3, None, None, 3, None, None, 1, 2, 2, None, 1, 2, None, None, None, None, 2, 1, 2, None, None, None, None],
            [None, 1, 3, None, None, None, None, 3, 1, 1, None, 3, None, 3, 3, None, 2, None, None, 2, 2, None, 1, 3, 2, None, None, 1, 2, 2, None],
            [None, 1, None, 3, 3, 2, None, None, 2, None, None, None, 2, None, None, 3, 2, None, None, None, 1, None, 3, 1, 2, None, 3, None, None, None, 1],
            [None, 2, None, None, None, 1, None, None, None, None, None, 2, None, None, 1, 1, None, 2, None, 1, 3, 1, None, 3, 2, 1, None, None, 1, None, None],
            [1, None, None, 1, None, None, 3, None, None, 2, 2, None, None, 1, None, None, 3, None, None, None, 2, None, None, None, 1, 2, None, 3, None, 1, None],
            [None, 1, None, 1, 1, 3, 1, None, 1, 3, 1, None, 1, 1, None, 1, None, 3, 2, 3, None, None, 3, 2, None, 1, 1, None, None, 1, 1],
            [None, None, None, None, None, None, None, 1, None, None, None, None, None, None, None, None, None, None, 1, 1, None, None, None, 1, None, None, None, 1, None, None, None]
        ])

        expected_solution_str = (
            '╲╱╱╱╲╲╲╱╲╲╲╲╲╱╱╲╲╱╱╲╱╱╱╱╱╱╲╱╱╲\n'
            '╲╱╲╱╱╲╱╱╲╲╱╲╱╱╱╲╱╲╱╲╱╲╲╱╲╲╲╲╲╲\n'
            '╲╲╲╲╲╲╱╱╲╱╱╲╱╲╱╱╱╱╲╲╱╱╱╲╲╱╱╲╲╱\n'
            '╱╱╱╲╲╲╲╱╲╱╱╲╲╲╲╱╲╲╲╲╲╲╱╱╱╱╱╱╱╲\n'
            '╲╱╱╱╲╱╲╲╲╱╱╲╱╱╲╲╲╱╱╱╱╲╱╲╱╱╲╲╱╱\n'
            '╱╱╱╱╲╱╲╱╱╲╱╲╲╱╱╲╲╱╱╱╱╲╱╱╲╱╱╱╲╲\n'
            '╱╲╲╱╲╲╲╱╱╲╱╲╱╱╱╱╲╲╲╲╱╱╱╲╲╱╲╱╲╱\n'
            '╱╲╲╱╱╱╲╲╱╲╱╱╱╱╲╲╲╱╲╲╱╱╱╲╲╱╱╲╲╲\n'
            '╲╲╲╲╲╱╲╲╱╱╲╲╱╱╱╱╲╲╲╱╲╲╱╲╲╲╱╲╱╱\n'
            '╱╲╲╱╲╲╲╲╱╱╲╲╲╲╱╲╲╱╱╱╱╱╱╱╲╲╱╱╱╲\n'
            '╱╱╲╲╲╲╱╲╱╲╲╱╲╲╱╲╲╱╱╲╲╱╱╱╲╲╲╱╱╲\n'
            '╲╱╱╲╲╲╲╲╱╲╲╱╲╲╱╲╲╱╱╱╱╱╲╲╲╲╲╲╲╲\n'
            '╱╲╱╱╲╱╲╱╱╲╱╱╱╱╱╲╱╲╲╱╱╲╲╱╱╱╱╱╱╱\n'
            '╲╲╱╱╱╲╲╱╱╱╱╲╲╱╲╲╱╲╲╲╱╲╲╲╲╲╲╲╱╱\n'
            '╱╱╱╱╱╲╱╲╲╱╱╱╲╱╲╲╱╱╱╲╱╲╱╱╲╲╲╱╲╲\n'
            '╲╲╲╱╱╱╲╲╱╱╱╱╱╱╱╱╱╱╲╲╲╲╱╱╱╱╱╱╲╱\n'
            '╲╱╲╱╱╱╲╱╱╲╲╲╲╲╱╱╲╲╲╱╱╲╱╱╲╲╱╱╲╱\n'
            '╱╱╲╲╲╲╲╱╱╱╲╱╱╱╲╲╲╲╱╲╱╲╲╲╲╲╲╱╱╲\n'
            '╱╱╱╱╲╲╱╲╲╱╱╱╱╲╲╱╲╲╱╱╱╱╱╲╱╱╲╱╲╲\n'
            '╱╱╱╱╱╱╲╲╱╲╱╲╱╲╱╱╱╱╲╱╱╱╲╲╲╲╲╲╲╱\n'
            '╲╱╱╲╱╱╱╲╲╲╱╱╲╲╱╲╲╲╲╱╱╱╱╱╲╱╱╲╱╲\n'
            '╲╲╱╱╲╲╱╱╲╲╲╱╲╲╲╲╲╱╲╱╱╲╲╱╲╲╱╲╲╲\n'
            '╲╲╲╱╲╱╱╲╲╱╲╱╱╲╲╲╲╱╲╱╱╲╲╱╲╱╲╲╱╱\n'
            '╱╲╱╱╱╲╲╲╲╲╲╱╱╱╲╲╲╱╲╱╱╲╲╱╱╲╲╱╲╱\n'
            '╱╲╲╲╱╱╲╱╲╲╲╲╲╱╱╱╱╲╲╱╱╱╱╱╱╱╱╲╲╲\n'
            '╱╱╲╱╱╱╲╲╲╱╱╲╱╱╲╱╱╲╲╱╱╲╱╲╲╲╱╱╱╱\n'
            '╲╱╱╱╲╲╲╲╲╲╲╲╱╱╲╲╲╲╱╲╱╱╱╱╱╲╲╱╲╱\n'
            '╲╱╱╲╲╱╱╱╲╱╲╲╱╲╲╱╱╱╲╲╲╱╱╲╲╲╲╱╱╲\n'
            '╲╲╱╱╲╱╲╱╲╱╲╱╲╲╱╱╲╲╲╱╱╲╲╲╱╱╲╲╱╱\n'
            '╲╱╲╱╱╱╱╱╱╱╱╲╲╱╲╱╱╲╲╲╱╱╲╲╲╱╱╱╲╱\n'
        )

        solver = SlantSolver(grid_clues)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_50x50_2025_12(self):
        grid_clues = Grid([
            [None, None, None, None, None, None, None, None, None, 1, None, None, None, None, None, 1, 1, 1, 1, None, None, None, None, 1, 1, None, None, None, 1, None, 1, None, 1, 1, 1, 1, None, None, None, None, None, None, None, 1, None, None, None, 1, None, None, None],
            [None, 2, 2, 3, 2, None, 2, 1, None, None, 3, None, 2, None, 2, None, 2, None, 3, None, 1, 3, 2, None, 3, None, 1, 2, 2, None, 2, 1, 2, None, None, None, None, 1, 1, None, 2, 1, 2, None, 2, None, None, 2, 2, 1, None],
            [None, 1, 2, 1, None, 1, 1, 2, 2, 3, None, None, 2, 3, 1, None, None, 2, 2, None, 3, None, 2, None, 2, 1, 3, 2, None, None, None, 1, 3, 1, None, 3, None, 1, None, None, None, None, 3, 3, None, 2, None, None, 3, 2, None],
            [None, None, None, None, None, 2, 3, 2, None, None, None, 3, 3, None, 1, None, 1, 3, None, None, 2, None, 1, 2, None, None, 2, 2, None, 1, None, 2, None, 2, None, 3, None, None, None, None, 2, None, None, None, None, 1, 2, None, 2, None, None],
            [1, None, None, 3, None, 1, None, 3, 2, None, 3, 1, None, None, None, None, 3, 1, 2, None, None, 2, 2, None, None, None, 1, None, 2, 3, None, None, 2, None, 2, None, None, None, 2, 1, 2, None, 2, 2, None, 3, None, 2, 2, 3, None],
            [None, 1, 3, None, 2, None, 3, None, 1, None, None, None, 2, 3, 2, 2, None, 1, None, None, 1, 1, 2, 3, None, 2, None, None, None, 1, None, 3, 1, 3, 2, None, None, 2, 1, None, 1, None, 1, None, None, 2, None, 3, None, None, None],
            [1, 2, None, 1, None, 3, 1, 1, 3, None, None, None, None, None, 1, None, None, None, 2, None, 1, None, 2, None, None, 3, None, 3, None, None, 3, 1, 3, None, 3, None, None, 2, None, None, 1, 1, None, 2, 1, None, 2, None, None, 1, None],
            [None, None, 1, None, None, 2, None, None, 1, None, 1, 2, 1, 3, 3, 2, None, None, None, 1, None, 2, None, 3, 3, None, None, 2, None, None, 3, None, 1, None, 2, None, None, None, 2, 1, None, None, None, 3, None, 2, 2, 2, None, None, 1],
            [None, 1, None, 1, None, None, None, 1, None, 2, None, 3, 1, 3, None, None, 1, 3, 3, None, 2, None, None, None, 2, 3, 1, None, None, 2, None, None, None, 2, None, None, None, None, 2, 2, 2, None, 3, None, None, 1, None, 1, 1, 2, None],
            [None, 2, 1, None, 3, 1, 3, 2, None, None, 2, None, 3, None, None, None, None, None, None, None, 3, None, None, 2, None, None, 1, 3, 1, None, 2, 3, 2, 1, 1, 3, 3, None, 1, None, 2, 3, None, None, 3, None, 2, None, 2, None, None],
            [1, None, None, 3, None, None, 3, None, None, None, None, 1, None, None, 2, None, None, 1, None, 2, 1, 2, 1, None, 1, None, None, 1, None, None, None, 3, None, None, 2, 2, 2, None, None, None, 2, 2, None, None, None, None, 2, 3, None, None, None],
            [1, None, 2, 1, 2, None, None, 2, None, None, 1, 3, None, None, 1, None, 2, 1, None, None, 2, 2, 3, 1, 2, None, None, 2, 1, 1, 3, None, 2, None, None, None, None, None, 1, 2, None, 2, None, 3, None, 3, None, None, None, 3, None],
            [1, None, 1, None, 1, None, None, None, 2, 2, None, 2, 2, None, None, 3, None, None, 3, None, None, None, None, 2, None, 3, 2, None, 2, None, None, None, None, 1, None, None, None, 1, 3, 2, 2, None, None, 2, 2, None, 2, 3, 1, None, None],
            [None, 1, None, None, 1, 3, None, None, 3, None, None, None, 2, 2, 3, 3, None, None, None, 2, None, 2, None, 2, None, None, None, None, None, 1, 2, None, 1, 1, None, 1, 3, None, 1, None, None, None, None, None, 2, 1, None, None, 2, 3, None],
            [None, None, None, None, None, 3, None, 2, None, 2, None, None, None, None, 3, None, None, 1, 2, None, None, 3, 1, None, 2, 2, 2, None, 2, 3, None, None, None, None, 1, 2, None, 3, None, 1, None, 1, None, None, 2, 1, None, 2, 1, 1, None],
            [None, 1, 3, 3, None, None, None, 2, None, None, 1, 3, 1, None, None, None, None, 1, None, 3, 3, 1, 2, 3, None, None, None, 2, 3, None, None, 2, 1, None, None, None, None, 3, None, None, 2, None, 3, 1, None, 2, None, None, None, None, None],
            [None, 1, None, 3, 1, 2, None, 1, None, 2, None, 1, 1, None, 1, None, None, None, 2, None, None, 3, None, 1, None, 1, 3, None, None, 2, 2, None, 2, 1, None, 1, None, 1, None, 2, 2, None, None, 1, 2, None, None, 2, 2, None, 1],
            [None, None, None, None, 2, None, 3, None, 2, 1, None, 2, 2, 1, None, 2, 2, 3, None, 3, 3, None, 1, 3, None, 1, 2, None, 2, None, 1, 2, 2, 3, 2, None, 2, None, 2, 1, None, None, 2, None, None, 3, 1, 2, None, 2, None],
            [1, 1, None, 2, None, None, None, 2, 3, None, 2, None, 2, 2, None, None, None, None, None, None, None, None, None, None, None, None, None, 3, None, None, 3, 2, 2, None, 2, None, None, None, None, None, None, 3, 2, 2, None, 2, None, None, None, 2, None],
            [1, 2, None, None, 1, 2, None, 3, None, 2, None, None, 3, None, 2, None, None, 1, 2, None, None, None, 1, 2, None, None, 2, None, 2, None, 3, 1, 1, 3, 1, 3, None, 2, 2, 1, 2, None, None, None, None, None, 3, 1, 2, None, 1],
            [None, 2, 2, None, 1, None, 1, None, None, 2, 2, 2, 2, 2, 3, 2, None, 1, 3, None, 2, 1, 2, None, 2, 2, None, 2, None, None, None, None, None, None, None, None, 3, 1, 1, None, None, 2, 2, 2, None, 3, 1, 2, None, 2, None],
            [None, 3, None, 1, None, 2, None, 3, None, 2, 2, 2, 2, 3, None, 2, 2, None, 1, None, None, 1, 2, 2, 1, None, None, 2, 3, None, None, None, 3, 3, None, None, 2, None, 2, 1, None, None, None, 2, 1, 2, None, 1, 3, None, None],
            [None, 1, 3, None, 1, None, 2, 1, 2, 2, None, None, None, None, 3, None, None, 2, 1, None, 2, 2, 2, 1, None, None, 2, None, None, 2, None, 3, None, 2, 2, None, None, None, 2, None, None, None, None, 1, None, 2, None, 3, None, 1, None],
            [None, None, 3, 2, 2, None, None, None, None, 1, None, 3, None, 3, None, None, None, None, None, None, None, None, None, 2, None, None, 2, 2, None, 2, 1, 2, None, None, None, 2, None, None, 3, None, 2, 3, None, None, None, 3, 1, 1, None, None, 1],
            [1, 2, None, 1, None, None, None, None, None, None, 2, 2, 1, None, 1, 3, 2, 1, 2, None, None, 1, 2, None, 2, None, 2, None, 3, None, 3, 1, 1, None, 2, 1, None, None, None, 3, 3, None, 2, None, None, None, 3, None, None, 1, None],
            [None, 2, None, 2, None, 2, 1, None, 2, 2, None, None, 2, None, None, None, None, 3, 1, 2, 2, 2, None, None, None, 2, 1, 2, 3, 1, None, 2, None, None, None, 1, None, None, 3, 1, None, None, 2, 2, 2, None, None, 3, None, None, None],
            [1, None, None, None, None, 1, None, 1, 2, None, None, 1, 2, 3, None, None, 2, 1, 3, None, 2, None, None, 3, 2, None, 2, None, None, 2, None, None, 2, None, None, None, None, None, None, 2, 2, 2, None, 2, 2, None, None, None, 2, 3, None],
            [None, 3, 1, 1, None, 2, 1, None, 3, None, None, 2, None, 1, 2, 2, None, 3, 1, None, 3, None, 2, None, None, 3, None, None, None, 2, 1, 2, 3, None, 3, 2, None, None, 2, 3, 1, None, None, None, None, None, 2, 1, None, 3, None],
            [None, 1, 2, None, 1, None, 2, 1, None, 3, None, 1, 3, None, None, None, 1, 2, 3, None, 1, 2, None, 2, 1, None, 3, 2, 2, None, None, None, 2, 3, None, 1, None, None, None, 1, 1, None, None, None, None, 2, None, 3, 3, None, None],
            [None, 3, 3, 2, None, None, 2, None, 2, None, 3, None, None, None, 2, None, None, 1, None, 3, None, 3, 2, None, 2, None, None, None, 3, None, 2, 1, None, None, None, None, None, 3, None, 1, None, 1, 3, None, None, 3, 1, None, None, None, None],
            [None, None, None, 1, 2, None, 3, None, None, 3, None, 1, 2, None, 1, None, 1, 3, None, 3, 1, None, None, 2, None, 1, None, None, None, None, 2, None, 2, 1, 3, None, 3, None, None, 2, None, 3, 2, 3, None, 2, None, None, 2, 1, None],
            [1, None, 3, 2, 2, None, None, 1, None, None, 2, 3, 1, None, 2, 2, 1, None, 2, None, None, 2, 2, 1, None, 1, 2, 3, 3, None, None, None, 2, 3, 2, None, 2, 1, None, None, None, 2, 2, None, None, None, None, None, 3, None, 1],
            [None, 2, None, 2, None, 2, 2, None, 1, 3, None, 2, None, None, None, None, None, 2, 3, 1, None, None, 2, None, None, None, 3, 2, None, 3, 1, None, None, None, 2, 2, 2, 1, None, None, 1, 2, None, 2, 2, None, 3, 1, 2, None, None],
            [None, None, 2, None, None, 2, None, 3, None, 3, None, None, 3, 1, None, None, 2, 2, None, 2, 1, None, None, 1, None, None, None, None, None, None, 2, 2, None, None, 3, None, None, None, 3, None, None, None, None, 2, None, 2, None, 3, None, 1, None],
            [None, 1, None, 1, 3, 2, 2, 3, None, 2, None, 2, 2, None, 2, 3, None, None, 1, None, None, None, 2, None, None, 3, None, 2, None, None, None, 2, 3, 3, None, 2, 3, 2, None, None, None, None, 2, None, 3, 3, None, 3, 2, None, None],
            [1, None, 3, 2, None, 3, None, 2, None, None, 3, None, 2, 3, 3, None, 2, None, None, 2, 2, 3, None, 2, 1, None, None, 3, 2, None, 1, 2, 2, 1, None, None, None, None, None, 2, 1, 2, 3, None, None, None, None, None, 3, 3, None],
            [None, 3, None, 2, None, 2, 2, None, None, None, None, None, None, 2, None, None, None, None, None, None, None, 3, None, 2, 1, None, 2, 3, None, None, 2, 2, 1, None, None, 2, 2, None, None, 3, 2, 1, None, 1, 3, 2, 2, 2, None, 2, None],
            [1, None, None, None, 1, None, None, None, None, None, 2, 1, None, 2, 2, 2, None, None, 1, None, None, None, None, None, 2, 2, None, 1, 2, 2, None, None, None, None, 1, 2, None, 1, None, 1, None, 3, None, None, 1, None, 1, None, None, None, None],
            [None, None, 3, None, None, 2, None, 3, None, 2, None, 2, None, 2, 1, None, 2, 3, 2, None, None, 2, 3, None, None, None, None, 1, 3, None, None, None, None, 3, 1, None, 2, None, 3, None, None, None, None, 2, 2, 1, None, None, None, 1, None],
            [None, 3, None, 3, 1, None, None, 3, None, 2, 2, 2, 2, None, 1, 2, 3, 1, None, 2, 3, 2, 2, None, 1, None, None, None, None, None, None, 3, 3, None, None, None, None, None, None, 1, None, 1, 2, None, None, 2, 1, 3, 3, None, 1],
            [None, 1, None, 2, 1, None, None, 2, 3, 2, 1, None, 1, None, 2, None, None, 3, 2, None, 2, 2, None, 3, None, 1, 3, None, 2, None, None, None, None, None, 2, 3, 2, None, None, None, 3, None, None, 2, None, 3, None, 1, 2, None, 1],
            [None, 1, 1, 2, None, None, 3, None, None, None, 2, 1, 3, None, None, None, None, None, None, 2, None, None, 2, None, 2, 2, None, 1, 2, 1, None, 3, 3, 2, None, None, 3, 2, 2, 2, 1, 2, None, 2, 1, None, None, 2, 1, None, None],
            [None, 3, None, None, None, 2, 3, None, 3, 2, None, 2, 2, None, 2, None, 2, None, None, None, 2, 2, None, 3, 2, None, 1, 2, None, 2, None, None, None, None, None, None, None, 2, 1, None, None, 1, 2, None, None, 2, None, None, 1, 1, None],
            [1, 1, 2, 3, None, None, None, 3, 1, None, 3, None, 1, None, None, 3, None, None, None, None, None, None, 1, None, None, None, 3, 2, 1, 1, 3, None, 2, 3, 2, None, None, 3, 2, None, None, None, 2, None, 2, 3, 2, None, None, 2, None],
            [None, None, 2, None, 3, 2, None, None, 3, 2, None, 3, None, 1, None, 2, 1, None, 2, 1, 3, 1, 3, None, 1, None, 1, 1, None, None, 1, 2, None, 2, None, 2, None, 2, None, None, 3, 2, None, None, 2, None, None, 2, None, 3, None],
            [None, 2, None, 1, None, None, 3, None, None, 3, None, 3, 2, None, 2, 2, None, None, None, 2, 1, None, 2, 2, None, None, None, None, None, 3, None, 2, None, 3, 3, None, 2, None, 3, 3, None, None, None, None, None, None, 1, None, None, None, None],
            [None, 2, None, None, 1, None, None, None, 2, None, 3, None, None, None, 2, 3, None, 3, 2, None, None, 2, 2, None, None, None, 1, 2, None, None, None, 2, 3, 2, None, None, 2, None, 2, None, 3, 1, None, None, 3, 3, None, 2, None, None, 1],
            [1, None, 2, 1, 2, None, None, 1, None, 2, None, None, 1, 2, None, 2, None, 3, None, 2, 2, 2, None, 3, 1, 1, None, 3, None, 1, 2, 2, None, None, 1, 2, None, None, None, None, 1, 2, None, None, None, None, 3, 3, 2, 2, None],
            [1, None, 1, None, 1, None, None, None, 1, None, None, 1, None, 1, None, 2, None, None, 3, None, None, None, None, 2, None, 2, None, 1, None, None, 1, None, None, 2, 3, 2, 3, None, 2, 2, None, 1, None, 2, 2, 2, None, None, 2, None, None],
            [None, 1, None, 1, None, None, 1, None, 2, 1, None, 1, 2, None, 1, 1, None, 1, None, None, None, 3, 2, None, 2, 1, 3, None, 2, 2, 2, None, None, None, None, None, 1, 1, 3, None, 3, 2, None, 2, 3, 1, None, None, 1, 3, None],
            [None, None, None, None, 1, 1, None, 1, None, None, None, None, 1, None, None, None, 1, None, 1, None, None, None, None, None, None, None, None, None, 1, 1, None, 1, None, 1, 1, 1, None, None, None, None, None, None, None, None, 1, None, 1, None, None, 1, None]
        ])

        expected_solution_str = (
            '╲╲╲╲╱╱╱╲╲╲╱╲╱╱╲╲╲╲╲╱╲╱╲╲╲╱╲╲╲╱╱╲╲╲╲╲╱╲╲╱╱╲╱╱╱╱╲╲╱╲\n'
            '╱╱╱╲╱╲╲╲╲╲╲╲╱╱╲╱╱╱╲╱╱╱╲╱╲╲╲╲╲╱╱╱╱╲╲╱╲╲╱╲╲╲╱╱╱╱╲╲╱╱\n'
            '╲╱╱╱╲╲╱╱╱╲╲╲╱╲╲╱╱╱╲╱╲╱╲╱╲╱╲╲╱╲╲╱╲╲╱╱╲╱╱╱╲╱╱╲╱╱╲╱╱╱\n'
            '╱╱╱╱╲╲╲╲╲╲╱╲╲╲╱╲╱╲╲╱╲╲╲╱╲╱╲╲╲╲╲╱╱╱╱╲╲╱╱╱╲╱╱╱╲╱╲╱╱╱\n'
            '╱╲╱╲╲╱╱╲╲╲╲╲╲╱╲╲╲╲╲╱╲╲╲╱╲╱╱╱╱╲╲╲╲╱╱╲╱╲╲╱╲╲╲╲╲╲╲╱╱╲\n'
            '╲╲╲╲╲╱╲╲╱╱╲╱╱╱╲╲╲╱╱╲╲╱╱╱╲╱╲╱╲╲╱╲╱╱╱╱╱╲╱╱╱╲╱╱╲╲╲╲╱╲\n'
            '╲╲╲╱╲╲╲╱╱╱╱╱╲╱╱╱╱╱╱╲╱╲╲╱╱╱╲╲╲╱╱╱╱╱╲╲╱╲╲╲╱╱╱╱╱╱╱╱╲╲\n'
            '╱╲╱╱╲╲╱╲╱╲╱╱╱╱╲╲╲╲╱╱╱╲╱╱╲╱╲╲╱╱╲╲╱╱╲╱╲╲╲╱╱╱╱╲╱╱╱╱╲╲\n'
            '╱╱╲╱╱╲╱╱╱╲╱╲╱╲╲╲╱╲╲╲╲╲╲╱╲╲╲╲╲╲╲╱╱╱╲╱╱╲╲╱╱╱╲╲╲╱╲╱╱╱\n'
            '╲╲╲╱╲╲╲╲╲╲╱╱╱╱╲╲╱╲╱╱╲╲╲╱╲╲╱╲╱╲╲╲╲╱╱╱╲╲╱╱╱╲╲╱╲╱╲╱╱╱\n'
            '╲╱╱╱╲╱╲╲╱╱╲╱╱╱╲╱╲╲╲╲╲╲╱╲╲╲╱╱╱╲╱╲╲╱╱╱╲╱╲╱╱╲╲╱╲╱╲╲╲╱\n'
            '╲╲╲╱╲╲╲╲╱╲╲╲╲╲╲╱╲╱╱╲╲╲╲╲╲╲╲╲╱╱╱╱╱╲╲╱╱╲╲╱╱╲╲╲╲╲╲╱╲╲\n'
            '╲╲╱╲╲╱╲╲╱╲╲╲╲╲╱╱╱╱╲╲╱╱╱╱╱╲╲╲╱╲╲╱╲╲╱╲╱╱╲╱╱╲╱╱╱╲╲╲╲╲\n'
            '╲╱╲╲╱╱╱╲╲╲╲╱╱╱╱╲╱╲╲╲╱╱╲╲╲╲╲╲╲╲╲╲╲╱╲╲╲╱╱╲╱╲╲╱╱╱╱╱╱╲\n'
            '╱╲╲╱╱╲╱╲╱╱╱╱╲╱╲╲╲╲╲╲╱╲╲╱╱╱╱╱╱╲╲╱╲╲╲╲╲╲╲╲╲╲╱╲╲╱╲╲╱╱\n'
            '╱╱╲╲╲╲╱╲╱╲╱╲╲╱╲╱╲╱╱╲╲╲╲╲╱╲╱╱╲╲╲╱╱╱╱╲╱╲╲╲╲╱╱╱╲╱╱╱╱╲\n'
            '╲╱╱╲╱╱╱╱╱╲╲╲╱╲╲╲╲╲╲╲╱╲╲╱╲╲╲╱╱╱╱╲╲╱╱╱╲╲╲╲╲╲╲╱╲╱╲╲╲╲\n'
            '╱╲╲╲╱╱╲╲╲╲╲╲╱╱╱╱╱╲╱╲╲╲╱╱╲╱╱╱╱╲╱╲╲╲╲╱╲╲╲╱╲╱╱╱╱╱╱╱╱╱\n'
            '╱╱╱╱╲╱╱╱╲╲╲╲╱╱╱╲╱╲╲╲╱╱╲╲╲╱╱╲╱╱╱╲╲╲╲╱╱╲╲╲╲╲╲╲╱╱╱╲╱╱\n'
            '╱╱╱╲╲╱╱╲╲╲╱╱╱╱╱╱╲╲╲╱╱╲╲╲╲╲╲╲╱╱╲╲╱╲╱╱╱╲╲╱╱╲╱╱╲╱╲╲╱╱\n'
            '╱╱╱╲╱╲╱╱╲╲╱╱╱╱╲╲╲╱╲╱╱╱╱╲╲╲╲╲╱╱╲╲╱╱╱╱╲╲╱╲╱╲╱╱╱╱╱╱╱╱\n'
            '╱╲╱╱╱╲╱╲╲╲╱╱╱╲╲╲╲╲╲╱╲╱╱╲╱╱╲╲╲╲╲╱╱╲╱╱╲╲╱╱╱╲╲╲╱╱╲╱╲╲\n'
            '╲╲╲╲╱╲╱╱╱╱╲╱╱╱╲╲╲╲╱╱╲╱╱╱╱╱╲╲╱╱╲╲╱╲╱╲╲╲╱╲╱╱╲╱╱╱╲╲╲╱\n'
            '╱╱╲╲╱╱╲╲╲╱╱╱╱╲╲╱╱╲╲╱╱╲╲╲╱╱╲╲╱╱╱╱╲╲╱╲╱╲╲╲╱╲╲╱╱╲╲╱╱╱\n'
            '╱╱╲╱╱╱╱╲╱╲╲╲╱╲╱╱╱╱╱╲╲╲╲╲╱╱╲╱╱╱╲╱╱╲╱╱╲╲╱╲╲╲╲╲╱╱╲╱╲╱\n'
            '╱╱╲╱╲╲╱╲╱╲╱╲╱╱╲╱╱╲╱╲╲╲╲╱╲╲╲╱╲╱╲╱╱╲╲╱╱╱╱╱╲╲╲╲╱╱╲╲╲╱\n'
            '╱╱╱╲╲╱╲╲╱╱╲╲╱╲╲╱╱╱╱╲╲╲╱╱╲╱╱╲╲╱╲╲╲╲╲╲╲╱╱╱╲╲╲╲╱╱╱╲╲╲\n'
            '╱╲╱╱╲╱╱╲╲╱╲╲╲╲╲╱╱╲╱╱╲╲╱╲╲╲╱╲╲╱╱╱╲╱╲╲╱╱╱╲╲╲╱╲╲╲╲╲╱╲\n'
            '╲╲╱╱╱╲╲╲╲╲╲╱╲╱╲╲╱╲╲╱╱╱╱╲╱╱╱╲╲╱╱╱╲╲╲╱╱╱╲╲╱╲╱╱╱╱╱╲╲╲\n'
            '╱╲╲╲╲╲╲╲╲╱╲╲╲╱╲╱╲╲╱╱╱╲╲╲╱╲╱╱╲╲╲╱╱╲╱╲╱╲╲╱╲╲╲╱╱╲╱╲╱╲\n'
            '╱╲╲╱╱╱╲╲╱╱╲╱╱╱╱╱╱╲╱╲╱╱╱╱╲╲╲╱╱╱╱╱╱╱╱╱╱╲╲╱╱╲╲╲╱╲╲╲╱╱\n'
            '╱╱╲╱╱╱╲╱╲╱╲╲╱╲╲╲╱╲╱╱╲╲╲╱╲╱╱╱╲╱╲╱╱╲╲╲╲╲╲╱╱╲╲╲╲╲╲╲╲╱\n'
            '╲╲╲╱╱╱╲╱╱╱╲╲╱╱╱╱╱╲╲╱╲╱╱╲╲╱╲╲╲╲╲╲╲╲╲╲╲╱╱╲╱╲╲╲╲╱╲╱╱╲\n'
            '╱╲╲╲╱╱╱╱╱╲╲╲╲╱╱╱╱╲╲╱╱╱╱╱╲╱╲╱╱╲╲╲╲╱╲╱╱╱╲╲╲╲╲╲╲╱╱╱╱╱\n'
            '╲╲╲╱╱╱╱╲╱╲╲╲╲╱╱╲╲╲╱╲╲╱╱╱╲╲╲╱╱╱╱╱╲╲╲╱╲╲╲╱╲╲╲╱╲╲╱╲╲╱\n'
            '╲╱╲╱╱╲╱╲╱╱╲╱╱╱╲╲╲╲╱╲╲╲╱╱╱╱╱╱╱╲╱╱╲╱╲╱╱╲╲╱╱╱╲╲╲╱╱╱╲╲\n'
            '╲╲╲╱╱╲╱╱╲╱╱╲╱╱╲╲╲╱╲╲╱╲╲╲╱╱╱╲╱╲╱╱╱╱╲╱╱╲╲╲╲╱╲╱╲╱╱╱╱╱\n'
            '╲╲╲╲╱╱╲╱╱╱╱╱╱╱╲╲╱╱╱╲╲╲╲╲╱╱╲╲╱╲╱╲╲╲╲╱╲╲╲╱╱╱╲╱╱╲╱╱╱╲\n'
            '╱╱╲╱╲╲╲╲╱╱╱╱╲╲╲╲╱╲╲╲╱╱╲╱╲╲╲╱╱╲╲╲╱╲╱╱╲╱╲╲╱╲╲╱╱╱╲╱╱╱\n'
            '╱╲╲╲╲╲╱╲╱╱╱╱╲╲╱╱╱╱╱╱╱╱╲╱╱╲╱╲╱╱╱╲╲╲╲╲╲╲╲╱╱╱╱╱╱╱╱╱╲╱\n'
            '╱╱╲╲╱╲╱╲╲╲╱╲╲╲╱╱╱╲╲╱╱╱╱╱╱╱╱╲╱╲╲╲╱╱╱╲╲╲╲╱╲╲╱╱╱╲╲╱╲╱\n'
            '╲╱╱╱╲╲╲╲╲╲╱╱╲╲╲╲╲╲╲╱╱╱╱╱╱╱╲╲╱╱╱╲╲╲╱╱╲╲╲╱╱╱╲╲╱╱╲╱╱╲\n'
            '╲╲╲╱╱╱╲╱╲╲╱╱╲╲╲╱╱╱╲╱╱╱╱╲╲╱╱╱╲╲╲╲╲╱╱╲╲╲╱╲╲╱╲╲╱╱╱╲╱╱\n'
            '╲╱╱╱╱╱╲╲╲╲╲╱╱╲╱╱╲╱╱╲╲╲╱╱╲╱╲╲╲╱╲╲╲╲╲╲╱╲╱╲╱╱╲╲╱╲╲╲╱╱\n'
            '╱╱╱╱╲╲╲╱╲╲╱╱╱╱╱╱╱╱╱╱╲╱╱╱╱╲╲╱╲╲╲╲╲╲╱╱╱╲╱╱╱╱╱╲╱╱╲╲╱╲\n'
            '╲╲╲╱╲╱╲╱╱╲╱╲╲╱╱╱╲╱╱╱╱╱╱╱╱╱╱╱╱╲╲╲╱╲╲╱╱╱╱╲╱╲╲╲╱╱╱╱╱╱\n'
            '╲╲╲╲╲╱╱╱╱╱╱╱╱╱╱╲╲╲╲╲╲╲╲╱╱╲╱╱╱╱╱╱╱╲╲╲╲╱╱╲╲╲╱╱╱╲╱╱╱╱\n'
            '╲╲╲╱╱╲╲╱╱╱╱╲╱╱╱╲╱╲╱╱╱╱╲╲╱╱╱╲╲╱╱╱╲╲╱╱╱╲╲╲╱╱╲╲╱╱╱╲╲╲\n'
            '╲╲╱╲╱╱╲╲╱╲╲╲╲╱╱╲╱╲╲╲╲╱╱╱╲╲╲╲╲╲╱╱╱╱╱╱╲╲╲╲╲╱╲╲╱╱╱╲╲╱\n'
            '╲╱╲╲╲╲╲╲╱╱╲╱╱╲╱╱╱╱╱╱╱╱╱╱╲╱╲╲╲╲╱╱╲╲╲╲╲╱╲╱╲╱╲╲╲╱╱╲╱╱\n'
        )

        solver = SlantSolver(grid_clues)
        solution = solver.get_solution()
        self.assertEqual(expected_solution_str, str(solution))
        other_solution = solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
