import unittest
from unittest import TestCase

from Domain.Grid.Grid import Grid
from Dominosa.DominosaSolver import DominosaSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine


class DominosaSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_not_min_grid(self):
        grid = Grid([[0, 0], [0, 1]])
        with self.assertRaises(ValueError) as context:
            DominosaSolver(grid, self.get_solver_engine())
        self.assertEqual("The grid must be at least 2x3", str(context.exception))

    def test_solution_not_r_c_grid(self):
        grid = Grid([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        with self.assertRaises(ValueError) as context:
            DominosaSolver(grid, self.get_solver_engine())
        self.assertEqual("The grid must be RxC with C = R + 1", str(context.exception))

    def test_solution_values_not_0_1(self):
        grid = Grid([[0, 1, 1], [1, 0, 2]])
        with self.assertRaises(ValueError) as context:
            DominosaSolver(grid, self.get_solver_engine())
        self.assertEqual("Values on dominoes must be between x and x + 1", str(context.exception))

    def test_solution_values_not_1_2_3(self):
        grid = Grid([[1, 2, 3, 4], [2, 3, 1, 1], [3, 1, 2, 1]])
        with self.assertRaises(ValueError) as context:
            DominosaSolver(grid, self.get_solver_engine())
        self.assertEqual("Values on dominoes must be between x and x + 2", str(context.exception))

    def test_solution_not_r_c_grid_2(self):
        grid = Grid([[0, 1, 0], [1, 0, 1]])
        solution = DominosaSolver(grid, self.get_solver_engine()).get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_2x3(self):
        grid = Grid([[0, 1, 1], [1, 0, 0]])

        expected_grid = Grid([
            ['⊓', '⊏', '⊐'],
            ['⊔', '⊏', '⊐'],
        ])

        solution = DominosaSolver(grid, self.get_solver_engine()).get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_4x5(self):
        grid = Grid([
            [1, 3, 3, 0, 0],
            [1, 2, 2, 1, 0],
            [3, 0, 1, 2, 2],
            [3, 1, 0, 3, 2]
        ])

        expected_grid = Grid([
            ['⊓', '⊏', '⊐', '⊏', '⊐'],
            ['⊔', '⊏', '⊐', '⊓', '⊓'],
            ['⊏', '⊐', '⊓', '⊔', '⊔'],
            ['⊏', '⊐', '⊔', '⊏', '⊐'],
        ])

        solution = DominosaSolver(grid, self.get_solver_engine()).get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_4x5_2(self):
        grid = Grid([
            [0, 1, 0, 3, 2],
            [3, 1, 2, 0, 1],
            [1, 3, 0, 0, 2],
            [2, 2, 3, 3, 1]
        ])

        expected_grid = Grid([
            ['⊓', '⊓', '⊓', '⊏', '⊐'],
            ['⊔', '⊔', '⊔', '⊏', '⊐'],
            ['⊏', '⊐', '⊏', '⊐', '⊓'],
            ['⊏', '⊐', '⊏', '⊐', '⊔'],
        ])

        solution = DominosaSolver(grid, self.get_solver_engine()).get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_5x6(self):
        grid = Grid([
            [4, 0, 4, 3, 3, 3],
            [1, 4, 3, 4, 2, 1],
            [3, 4, 2, 0, 4, 0],
            [2, 0, 0, 0, 3, 1],
            [2, 2, 2, 1, 1, 1]
        ])

        expected_grid = Grid([
            ['⊓', '⊏', '⊐', '⊏', '⊐', '⊓'],
            ['⊔', '⊓', '⊏', '⊐', '⊓', '⊔'],
            ['⊓', '⊔', '⊏', '⊐', '⊔', '⊓'],
            ['⊔', '⊏', '⊐', '⊏', '⊐', '⊔'],
            ['⊏', '⊐', '⊏', '⊐', '⊏', '⊐'],
        ])

        solution = DominosaSolver(grid, self.get_solver_engine()).get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_6x7(self):
        grid = Grid([
            [3, 1, 2, 1, 4, 4, 0],
            [1, 5, 2, 1, 4, 3, 0],
            [0, 3, 3, 2, 4, 3, 5],
            [2, 3, 5, 2, 1, 5, 1],
            [2, 4, 0, 4, 2, 0, 0],
            [3, 4, 0, 5, 5, 5, 1]
        ])

        expected_grid = Grid([
            ['⊓', '⊏', '⊐', '⊓', '⊓', '⊏', '⊐'],
            ['⊔', '⊏', '⊐', '⊔', '⊔', '⊓', '⊓'],
            ['⊏', '⊐', '⊓', '⊓', '⊓', '⊔', '⊔'],
            ['⊏', '⊐', '⊔', '⊔', '⊔', '⊏', '⊐'],
            ['⊏', '⊐', '⊓', '⊓', '⊏', '⊐', '⊓'],
            ['⊏', '⊐', '⊔', '⊔', '⊏', '⊐', '⊔'],
        ])

        solution = DominosaSolver(grid, self.get_solver_engine()).get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_7x8(self):
        grid = Grid([
            [3, 3, 5, 2, 6, 4, 6, 5],
            [5, 6, 3, 4, 1, 4, 0, 5],
            [0, 6, 4, 2, 1, 6, 3, 2],
            [1, 0, 5, 2, 1, 6, 3, 1],
            [5, 4, 0, 0, 5, 6, 0, 4],
            [2, 3, 1, 3, 3, 4, 2, 2],
            [6, 0, 2, 0, 4, 1, 1, 5]
        ])

        expected_grid = Grid([
            ['⊓', '⊓', '⊏', '⊐', '⊓', '⊓', '⊓', '⊓'],
            ['⊔', '⊔', '⊏', '⊐', '⊔', '⊔', '⊔', '⊔'],
            ['⊓', '⊏', '⊐', '⊓', '⊓', '⊓', '⊏', '⊐'],
            ['⊔', '⊏', '⊐', '⊔', '⊔', '⊔', '⊏', '⊐'],
            ['⊏', '⊐', '⊏', '⊐', '⊏', '⊐', '⊓', '⊓'],
            ['⊓', '⊓', '⊓', '⊏', '⊐', '⊓', '⊔', '⊔'],
            ['⊔', '⊔', '⊔', '⊏', '⊐', '⊔', '⊏', '⊐'],
        ])

        solution = DominosaSolver(grid, self.get_solver_engine()).get_solution()
        self.assertEqual(expected_grid, solution)

    def test_solution_10x11(self):
        grid = Grid([
            [5, 2, 3, 8, 7, 5, 4, 7, 9, 0, 9],
            [3, 1, 2, 8, 6, 5, 7, 3, 2, 1, 6],
            [4, 0, 1, 8, 2, 1, 5, 7, 7, 8, 9],
            [2, 1, 4, 9, 0, 1, 9, 5, 4, 8, 2],
            [6, 0, 3, 0, 3, 7, 1, 6, 8, 4, 2],
            [3, 5, 5, 2, 0, 6, 8, 3, 9, 5, 8],
            [6, 5, 0, 2, 1, 5, 4, 9, 6, 3, 3],
            [7, 7, 8, 7, 5, 4, 9, 9, 6, 1, 9],
            [4, 8, 6, 4, 0, 2, 6, 6, 7, 4, 4],
            [3, 7, 0, 1, 0, 2, 3, 9, 0, 8, 1],
        ])

        expected_grid = Grid([
            ['⊏', '⊐', '⊏', '⊐', '⊓', '⊓', '⊓', '⊏', '⊐', '⊏', '⊐'],
            ['⊏', '⊐', '⊏', '⊐', '⊔', '⊔', '⊔', '⊓', '⊓', '⊏', '⊐'],
            ['⊏', '⊐', '⊓', '⊓', '⊓', '⊓', '⊓', '⊔', '⊔', '⊓', '⊓'],
            ['⊏', '⊐', '⊔', '⊔', '⊔', '⊔', '⊔', '⊏', '⊐', '⊔', '⊔'],
            ['⊓', '⊓', '⊓', '⊏', '⊐', '⊏', '⊐', '⊏', '⊐', '⊏', '⊐'],
            ['⊔', '⊔', '⊔', '⊓', '⊏', '⊐', '⊓', '⊏', '⊐', '⊏', '⊐'],
            ['⊏', '⊐', '⊓', '⊔', '⊏', '⊐', '⊔', '⊓', '⊓', '⊏', '⊐'],
            ['⊏', '⊐', '⊔', '⊏', '⊐', '⊏', '⊐', '⊔', '⊔', '⊏', '⊐'],
            ['⊓', '⊓', '⊏', '⊐', '⊓', '⊏', '⊐', '⊓', '⊓', '⊏', '⊐'],
            ['⊔', '⊔', '⊏', '⊐', '⊔', '⊏', '⊐', '⊔', '⊔', '⊏', '⊐']
        ])

        solution = DominosaSolver(grid, self.get_solver_engine()).get_solution()
        self.assertEqual(expected_grid, solution)


if __name__ == '__main__':
    unittest.main()
