import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Puzzles.Thermometers.ThermometersSolver import ThermometersSolver


class ThermometersSolverTests(TestCase):
    def test_solution_grid_not_a_square(self):
        grid = Grid([
            [0, 1, 1, 1],
            [0, 2, 2, 1],
            [0, 2, 2, 1],
            [0, 2, 2, 1],
            [0, 2, 2, 1],
        ])
        full_by_column_row = {'column': [1, 1, 1, 1], 'row': [1, 1, 1, 1, 1]}
        with self.assertRaises(ValueError) as context:
            ThermometersSolver(grid, full_by_column_row)
        self.assertEqual("The grid must be square", str(context.exception))

    def test_solution_grid_size_less_than_4(self):
        grid = Grid([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ])
        full_by_column_row = {'column': [1, 1, 1], 'row': [1, 1, 1]}
        with self.assertRaises(ValueError) as context:
            ThermometersSolver(grid, full_by_column_row)
        self.assertEqual("The grid must be at least 4x4", str(context.exception))

    def test_solution_with_sum_thermometer_cells_constraint(self):
        grid = Grid([
            ['c1', 'l1', 'l1', 'e3'],
            ['s4', 'c1', 'c2', 's2'],
            ['s1', 'c3', 'e4', 'l2'],
            ['e1', 'l1', 'l1', 'c3'],
        ])
        full_by_column_row = {'column': [2, 0, 1, 3], 'row': [1, 2, 1, 2]}
        game_solver = ThermometersSolver(grid, full_by_column_row)
        solution = game_solver.get_solution()
        self.assertTrue(all([full_by_column_row['row'][i] == sum(row) for i, row in enumerate(solution.matrix)]))
        self.assertTrue(all([full_by_column_row['column'][i] == sum(column) for i, column in enumerate(zip(*solution.matrix))]))

    def test_solution_empty(self):
        grid = Grid([
            ['c1', 'l1', 'l1', 'e3'],
            ['s4', 'c1', 'c2', 's2'],
            ['s1', 'c3', 'e4', 'l2'],
            ['e1', 'l1', 'l1', 'c3'],
        ])
        full_by_column_row = {'column': [1, 0, 0, 0], 'row': [1, 0, 0, 0]}
        game_solver = ThermometersSolver(grid, full_by_column_row)
        solution = game_solver.get_solution()
        self.assertEqual(Grid.empty(), solution)

    def test_solution_4x4(self):
        grid = Grid([
            ['c1', 'l1', 'l1', 'e3'],
            ['s4', 'c1', 'c2', 's2'],
            ['s1', 'c3', 'e4', 'l2'],
            ['e1', 'l1', 'l1', 'c3'],
        ])
        full_by_column_row = {'column': [2, 0, 1, 3], 'row': [1, 2, 1, 2]}
        expected_solution = Grid([
            [1, 0, 0, 0],
            [1, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 1, 1],
        ])
        game_solver = ThermometersSolver(grid, full_by_column_row)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_6x6(self):
        grid = Grid([
            ['c1', 'c2', 'c1', 'e3', 'e1', 'c2'],
            ['s4', 'e4', 'c4', 's3', 's1', 'c3'],
            ['c1', 'e3', 'e1', 'l1', 's3', 's2'],
            ['c4', 'l1', 'l1', 'l1', 's3', 'l2'],
            ['c1', 's3', 'e1', 'l1', 's3', 'l2'],
            ['c4', 'l1', 'l1', 'e3', 'e1', 'c3']
        ])
        full_by_column_row = {'column': [4, 2, 1, 2, 4, 4], 'row': [2, 5, 3, 2, 3, 2]}
        expected_solution = Grid([
            [1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1],
            [0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 0],
            [1, 1, 0, 0, 0, 0],
        ])
        game_solver = ThermometersSolver(grid, full_by_column_row)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_10x10(self):
        grid = Grid([
            ['e2', 'e1', 'c2', 'c1', 'l1', 'l1', 'l1', 'l1', 'l1', 'c2'],
            ['s4', 's1', 'c3', 'c4', 'c2', 'e1', 'l1', 'l1', 's3', 'l2'],
            ['e1', 'l1', 'l1', 'l1', 'c3', 'c1', 'l1', 'l1', 's3', 'l2'],
            ['s2', 'c1', 'l1', 'l1', 's3', 'c4', 'e3', 's2', 's2', 'l2'],
            ['l2', 'c4', 'e3', 'e1', 'l1', 'l1', 'l1', 'c3', 'e4', 'l2'],
            ['l2', 'e2', 's2', 'c1', 'l1', 'l1', 'l1', 'e3', 'e2', 'l2'],
            ['l2', 'l2', 'l2', 'c4', 'l1', 'l1', 'l1', 'c2', 'l2', 's4'],
            ['c4', 'c3', 'c4', 'l1', 'l1', 'l1', 'l1', 'c3', 's4', 's2'],
            ['c1', 'c2', 'c1', 'l1', 'l1', 'l1', 'l1', 'l1', 's3', 'l2'],
            ['s4', 'e4', 'c4', 'e3', 'e1', 'l1', 'l1', 'l1', 'l1', 'c3']
        ])
        full_by_column_row = {'column': [5, 1, 6, 5, 5, 4, 6, 8, 4, 5], 'row': [1, 4, 4, 5, 3, 5, 8, 8, 7, 4]}
        expected_solution = Grid([
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
            [1, 0, 1, 1, 1, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
            [1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        ])
        game_solver = ThermometersSolver(grid, full_by_column_row)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15(self):
        grid = Grid([
            ['e2', 'c1', 's3', 'c1', 'l1', 'l1', 's3', 's1', 'l1', 'l1', 'l1', 'c2', 'c1', 'c2', 'e2'],
            ['l2', 'c4', 'e3', 'e4', 'e1', 'l1', 'l1', 'l1', 'c2', 's2', 'c1', 'c3', 'l2', 'l2', 'l2'],
            ['c4', 'l1', 'l1', 'l1', 's3', 'e1', 'l1', 'c2', 'l2', 'l2', 'c4', 'e3', 'l2', 'l2', 'l2'],
            ['s1', 'l1', 'l1', 'l1', 'l1', 'l1', 'l1', 'c3', 'l2', 'l2', 'c1', 'c2', 'l2', 'l2', 'l2'],
            ['c1', 'l1', 'e3', 's1', 'l1', 'e3', 's1', 'l1', 'c3', 'l2', 'l2', 'l2', 'l2', 'l2', 'l2'],
            ['c4', 's3', 'c1', 'l1', 'l1', 'l1', 'e3', 'e1', 's3', 'l2', 'e4', 's4', 's4', 'l2', 'l2'],
            ['c1', 's3', 'c4', 'l1', 'l1', 'l1', 'l1', 'l1', 's3', 'l2', 's2', 'c1', 'c2', 'l2', 'l2'],
            ['e4', 'e1', 'l1', 'l1', 'l1', 'l1', 'l1', 'l1', 'c2', 'l2', 'c4', 'c3', 'e4', 'e4', 'l2'],
            ['s1', 'l1', 'c2', 'c1', 'l1', 'l1', 'l1', 'l1', 'c3', 'c4', 'e3', 's1', 'l1', 'e3', 'l2'],
            ['c1', 'c2', 'e4', 'c4', 'l1', 's3', 's1', 'l1', 'l1', 'l1', 'l1', 'e3', 'e1', 'c2', 'l2'],
            ['l2', 'l2', 'e1', 's3', 's1', 'l1', 'l1', 'l1', 'l1', 'c2', 'c1', 'l1', 'l1', 'c3', 'l2'],
            ['s4', 'c4', 'l1', 'l1', 'l1', 'l1', 'l1', 'e3', 'e1', 'c3', 'c4', 'l1', 'l1', 'c2', 'l2'],
            ['s1', 'c2', 'c1', 'e3', 'e1', 'l1', 'l1', 'l1', 'l1', 'l1', 'l1', 'c2', 's2', 'l2', 'l2'],
            ['s2', 'e4', 'l2', 'c1', 'c2', 's1', 'l1', 'e3', 's1', 'l1', 'c2', 'l2', 'l2', 'l2', 's4'],
            ['c4', 'e3', 's4', 's4', 'c4', 'e3', 'e1', 'l1', 'l1', 'l1', 'c3', 'c4', 'c3', 'c4', 's3']
        ])
        full_by_column_row = {'column': [9, 4, 8, 8, 9, 12, 9, 8, 11, 5, 4, 5, 9, 5, 6], 'row': [11, 10, 7, 9, 4, 5, 7, 4, 7, 6, 4, 3, 10, 12, 13]}
        expected_solution = Grid([
            [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        ])
        game_solver = ThermometersSolver(grid, full_by_column_row)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)

    def test_solution_15x15_2(self):
        grid = Grid([
            ['e1', 'l1', 'l1', 'c2', 'e1', 's3', 'c1', 'l1', 'l1', 'e3', 's1', 'l1', 'l1', 'l1', 'c2'],
            ['e2', 'e1', 'c2', 's4', 'c1', 'c2', 'c4', 's3', 'e1', 'l1', 'l1', 'l1', 'l1', 'l1', 'c3'],
            ['s4', 'e2', 's4', 'e2', 'l2', 'l2', 'c1', 'c2', 'c1', 'e3', 'e1', 'c2', 'c1', 'l1', 'c2'],
            ['e2', 'c4', 's3', 's4', 'l2', 'l2', 'l2', 'l2', 'l2', 'c1', 'c2', 's4', 's4', 'e2', 'l2'],
            ['s4', 'e2', 'e1', 's3', 'l2', 'l2', 'l2', 'l2', 'l2', 'e4', 'l2', 'c1', 'c2', 'c4', 'c3'],
            ['s2', 'c4', 'l1', 'c2', 'l2', 'l2', 'l2', 'l2', 'l2', 's2', 'l2', 'l2', 'e4', 's1', 'c2'],
            ['e4', 'c1', 's3', 'l2', 'l2', 'l2', 'l2', 'l2', 'l2', 'e4', 'l2', 'l2', 's1', 'e3', 'e4'],
            ['s2', 'c4', 'c2', 'l2', 'l2', 'l2', 'l2', 'l2', 'l2', 's2', 'l2', 'l2', 'c1', 'l1', 'e3'],
            ['l2', 'e2', 'l2', 'l2', 'l2', 'l2', 's4', 'l2', 'l2', 'l2', 's4', 'l2', 'c4', 'l1', 's3'],
            ['c4', 'c3', 'l2', 'l2', 'l2', 'l2', 's2', 'e4', 'l2', 'e4', 's2', 'l2', 'c1', 'l1', 'c2'],
            ['c1', 's3', 'l2', 'l2', 'l2', 'l2', 'c4', 'e3', 'l2', 'e2', 'l2', 'l2', 'l2', 'c1', 'c3'],
            ['c4', 'c2', 'l2', 'l2', 'l2', 'l2', 'e1', 'c2', 'l2', 'c4', 'c3', 's4', 'l2', 'e4', 's2'],
            ['e1', 'c3', 'c4', 'c3', 'l2', 'l2', 'e2', 's4', 's4', 's1', 'l1', 'l1', 'c3', 'e1', 'c3'],
            ['c1', 'e3', 'e1', 's3', 's4', 'l2', 'l2', 'e2', 'c1', 'l1', 'e3', 's1', 'l1', 'c2', 'e2'],
            ['c4', 'l1', 'l1', 'l1', 's3', 'c4', 'c3', 's4', 's4', 's1', 'l1', 'l1', 'e3', 'c4', 'c3']
        ])
        full_by_column_row = {'column': [7, 14, 13, 11, 14, 13, 8, 3, 4, 1, 10, 2, 7, 2, 3], 'row': [6, 6, 8, 6, 5, 7, 7, 8, 8, 11, 9, 12, 10, 4, 5]}
        expected_solution = Grid([
            [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
            [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0],
            [1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])
        game_solver = ThermometersSolver(grid, full_by_column_row)
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertEqual(Grid.empty(), other_solution)


if __name__ == '__main__':
    unittest.main()
