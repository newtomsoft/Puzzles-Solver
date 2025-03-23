import unittest
from unittest import TestCase

from Domain.Direction import Direction
from Domain.Grid.Grid import Grid
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine
from Stitches.StitchesSolver import StitchesSolver


class StitchesSolverTests(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def test_solution_grid_not_a_square(self):
        grid = Grid([
            [0, 1, 1, 1, 1, 1],
            [0, 2, 2, 1, 1, 1],
            [0, 2, 2, 1, 1, 1],
            [0, 2, 2, 1, 1, 1],
            [0, 2, 2, 1, 1, 1],
        ])
        dots_by_column_row = {'column': [1, 1, 1, 1, 1, 1, 1], 'row': [1, 1, 1, 1, 1, 1]}
        regions_connections = 1
        with self.assertRaises(ValueError) as context:
            StitchesSolver(grid, dots_by_column_row, regions_connections, self.get_solver_engine())
        self.assertEqual("The grid must be square", str(context.exception))

    def test_solution_grid_size_less_than_4(self):
        grid = Grid([
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
        ])
        dots_by_column_row = {'column': [1, 1, 1, 1], 'row': [1, 1, 1, 1]}
        regions_connections = 1
        with self.assertRaises(ValueError) as context:
            StitchesSolver(grid, dots_by_column_row, regions_connections, self.get_solver_engine())
        self.assertEqual("The grid must be at least 5x5", str(context.exception))

    def test_solution_regions_connections_less_than_1(self):
        grid = Grid([
            [0, 1, 1, 1, 1],
            [0, 2, 2, 1, 1],
            [0, 2, 2, 1, 1],
            [0, 2, 2, 1, 1],
            [0, 2, 2, 1, 1],
        ])
        dots_by_column_row = {'column': [1, 1, 1, 1, 1], 'row': [1, 1, 1, 1, 1]}
        regions_connections = 0
        with self.assertRaises(ValueError) as context:
            StitchesSolver(grid, dots_by_column_row, regions_connections, self.get_solver_engine())
        self.assertEqual("The grid must require at least 1 connection between regions", str(context.exception))

    def test_solution_regions_less_2(self):
        grid = Grid([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])
        dots_by_column_row = {'column': [1, 1, 1, 1, 1], 'row': [1, 1, 1, 1, 1]}
        regions_connections = 1
        with self.assertRaises(ValueError) as context:
            StitchesSolver(grid, dots_by_column_row, regions_connections, self.get_solver_engine())
        self.assertEqual("The grid must have at least 2 regions", str(context.exception))

    def test_solution_dots_by_column_row_not_compliant(self):
        grid = Grid([
            [1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])
        dots_by_column_row = {'column': [1, 1, 1, 1, 1], 'row': [1, 1, 1, 1]}
        regions_connections = 1
        with self.assertRaises(ValueError) as context:
            StitchesSolver(grid, dots_by_column_row, regions_connections, self.get_solver_engine())
        self.assertEqual("The dots count must have the same size as the columns", str(context.exception))

    def test_solution_using_add_constraint_dots_in_rows_and_columns(self):
        grid = Grid([
            [8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [5, 0, 0, 0, 0],
        ])
        expected_dots = Grid([
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0],
        ])
        dots_by_column_row = {'column': [3, 1, 0, 0, 0], 'row': [1, 1, 0, 0, 2]}
        regions_connections = 1
        game_solver = StitchesSolver(grid, dots_by_column_row, regions_connections, self.get_solver_engine())
        solution = game_solver.get_solution()
        dots = Grid([[cell > 0 for cell in row] for row in solution.matrix])
        self.assertEqual(expected_dots, dots)
        other_solution = game_solver.get_other_solution()
        other_dots = Grid([[cell > 0 for cell in row] for row in other_solution.matrix])
        self.assertTrue(other_dots.is_empty() or other_dots == dots)

    def test_solution_adding_2_by_2_crossing_2_regions(self):
        grid = Grid([
            [8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 7],
            [0, 0, 0, 0, 0],
            [5, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [Direction._DOWN, 0, 0, 0, 0],
            [Direction._UP, 0, 0, 0, 0],
            [0, 0, 0, 0, Direction._DOWN],
            [0, 0, 0, 0, Direction._UP],
            [Direction._RIGHT, Direction._LEFT, 0, 0, 0],
        ])
        dots_by_column_row = {'column': [3, 1, 0, 0, 2], 'row': [1, 1, 1, 1, 2]}
        regions_connections = 1
        game_solver = StitchesSolver(grid, dots_by_column_row, regions_connections, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solution_adding_2_by_2_crossing_2_regions_2(self):
        grid = Grid([
            [1, 0, 0, 4, 4],
            [1, 0, 0, 4, 4],
            [0, 0, 0, 0, 0],
            [3, 3, 0, 0, 2],
            [3, 3, 0, 0, 2],
        ])
        expected_solution = Grid([
            [Direction._RIGHT, Direction._LEFT, 0, 0, 0],
            [0, 0, 0, Direction._DOWN, 0],
            [0, Direction._DOWN, 0, Direction._UP, 0],
            [0, Direction._UP, 0, 0, 0],
            [0, 0, 0, Direction._RIGHT, Direction._LEFT],
        ])
        dots_by_column_row = {'column': [1, 3, 0, 3, 1], 'row': [2, 1, 2, 1, 2]}
        regions_connections = 1
        game_solver = StitchesSolver(grid, dots_by_column_row, regions_connections, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solution_adding_2_by_2_crossing_2_regions_3(self):
        grid = Grid([
            [1, 0, 0, 4, 4],
            [1, 0, 0, 4, 4],
            [0, 0, 0, 0, 0],
            [3, 3, 0, 0, 2],
            [3, 3, 0, 0, 2],
        ])
        expected_solution = Grid([
            [2, 4, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 0, 3, 0],
            [0, 3, 0, 0, 0],
            [0, 0, 0, 2, 4],
        ])
        dots_by_column_row = {'column': [1, 3, 0, 3, 1], 'row': [2, 1, 2, 1, 2]}
        regions_connections = 1
        game_solver = StitchesSolver(grid, dots_by_column_row, regions_connections, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solution_2_connections(self):
        grid = Grid([
            [1, 1, 1, 1, 1],
            [2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2],
            [2, 2, 3, 2, 2],
            [2, 2, 3, 2, 2],
        ])
        expected_solution = Grid([
            [1, 0, 0, 0, 1],
            [3, 0, 0, 0, 3],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 4, 0],
            [0, 0, 2, 4, 0],
        ])
        dots_by_column_row = {'column': [2, 0, 2, 2, 2], 'row': [2, 2, 0, 2, 2]}
        regions_connections = 2
        game_solver = StitchesSolver(grid, dots_by_column_row, regions_connections, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solution_adding_regions_count(self):
        grid = Grid([
            [1, 1, 1, 1, 1],
            [1, 1, 2, 2, 1],
            [3, 3, 3, 3, 1],
            [3, 0, 0, 3, 3],
            [4, 4, 4, 4, 3],
        ])
        expected_solution = Grid([
            [0, 0, 0, 1, 0],
            [0, 0, 1, 3, 0],
            [0, 1, 3, 2, 4],
            [1, 3, 1, 0, 0],
            [3, 0, 3, 0, 0],
        ])
        dots_by_column_row = {'column': [2, 2, 4, 3, 1], 'row': [1, 2, 4, 3, 2]}
        regions_connections = 1
        game_solver = StitchesSolver(grid, dots_by_column_row, regions_connections, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solution_5x5_1(self):
        grid = Grid([
            [1, 0, 2, 0, 3],
            [1, 0, 2, 0, 3],
            [4, 0, 0, 0, 3],
            [4, 0, 0, 0, 3],
            [0, 0, 0, 0, 0],
        ])
        expected_solution = Grid([
            [2, 4, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [3, 0, 3, 0, 0],
            [1, 0, 0, 0, 1],
            [3, 0, 0, 0, 3],
        ])
        dots_by_column_row = {'column': [5, 1, 2, 0, 2], 'row': [2, 2, 2, 2, 2]}
        regions_connections = 1
        game_solver = StitchesSolver(grid, dots_by_column_row, regions_connections, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solution_5x5_2(self):
        grid = Grid([
            [1, 1, 2, 2, 3],
            [1, 2, 2, 3, 3],
            [1, 0, 0, 3, 4],
            [0, 0, 0, 3, 4],
            [0, 4, 4, 4, 4],
        ])
        expected_solution = Grid([
            [0, 2, 4, 1, 0],
            [0, 0, 1, 3, 1],
            [2, 4, 3, 0, 3],
            [0, 0, 2, 4, 0],
            [2, 4, 0, 0, 0],
        ])
        dots_by_column_row = {'column': [2, 3, 4, 3, 2], 'row': [3, 3, 4, 2, 2]}
        regions_connections = 1
        game_solver = StitchesSolver(grid, dots_by_column_row, regions_connections, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solution_5x5_3(self):
        grid = Grid([
            [1, 2, 2, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 4, 4, 1, 1],
            [3, 3, 4, 4, 0],
            [4, 4, 4, 0, 0],
        ])
        expected_solution = Grid([
            [0, 0, 2, 4, 0],
            [0, 1, 0, 0, 0],
            [1, 3, 0, 0, 1],
            [3, 2, 4, 0, 3],
            [0, 0, 2, 4, 0]
        ])
        dots_by_column_row = {'column': [2, 3, 3, 2, 2], 'row': [2, 1, 3, 4, 2]}
        regions_connections = 1
        game_solver = StitchesSolver(grid, dots_by_column_row, regions_connections, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solution_7x7(self):
        grid = Grid([
            [1, 2, 2, 2, 2, 2, 3],
            [1, 1, 1, 1, 3, 3, 3],
            [1, 1, 1, 1, 3, 6, 6],
            [3, 3, 3, 3, 3, 6, 5],
            [3, 3, 7, 7, 3, 6, 5],
            [4, 5, 7, 7, 6, 6, 5],
            [4, 5, 5, 5, 5, 5, 5],
        ])
        expected_solution = Grid([
            [2, 4, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 3, 0],
            [0, 0, 0, 2, 4, 0, 1],
            [0, 0, 0, 1, 0, 0, 3],
            [1, 1, 0, 3, 2, 4, 0],
            [3, 3, 1, 2, 4, 0, 0],
            [2, 4, 3, 0, 0, 0, 0],
        ])
        dots_by_column_row = {'column': [4, 4, 2, 4, 3, 3, 2], 'row': [3, 1, 3, 2, 5, 5, 3]}
        regions_connections = 1
        game_solver = StitchesSolver(grid, dots_by_column_row, regions_connections, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solution_7x7_2connections_1(self):
        grid = Grid([
            [1, 1, 1, 2, 2, 2, 2],
            [1, 2, 1, 2, 2, 3, 3],
            [1, 2, 2, 2, 2, 3, 4],
            [1, 5, 5, 2, 3, 3, 4],
            [1, 1, 5, 2, 3, 4, 4],
            [1, 5, 5, 5, 4, 4, 4],
            [1, 5, 5, 4, 4, 4, 4],
        ])
        expected_solution = Grid([
            [0, 0, 0, 0, 0, 0, 0],
            [2, 4, 2, 4, 2, 4, 1],
            [0, 1, 1, 0, 0, 0, 3],
            [0, 3, 3, 0, 0, 2, 4],
            [0, 1, 0, 2, 4, 0, 0],
            [0, 3, 0, 2, 4, 0, 0],
            [2, 4, 2, 4, 0, 0, 0]
        ])
        dots_by_column_row = {'column': [2, 6, 4, 4, 3, 2, 3], 'row': [0, 7, 3, 4, 3, 3, 4]}
        regions_connections = 2
        game_solver = StitchesSolver(grid, dots_by_column_row, regions_connections, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())

    def test_solution_7x7_2connections_2(self):
        grid = Grid([
            [1, 1, 1, 2, 2, 2, 2],
            [1, 1, 1, 2, 5, 2, 5],
            [1, 2, 1, 2, 5, 5, 5],
            [2, 2, 2, 2, 5, 3, 5],
            [2, 3, 3, 5, 5, 3, 3],
            [2, 3, 3, 3, 3, 3, 3],
            [3, 3, 4, 4, 4, 4, 4],
        ])
        expected_solution = Grid([
            [0, 0, 2, 4, 1, 0, 0],
            [0, 0, 0, 0, 3, 2, 4],
            [2, 4, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 3, 0],
            [0, 0, 3, 0, 2, 4, 0],
            [1, 0, 0, 1, 0, 0, 1],
            [3, 0, 0, 3, 0, 0, 3]
        ])
        dots_by_column_row = {'column': [3, 1, 3, 3, 3, 4, 3], 'row': [3, 3, 3, 2, 3, 3, 3]}
        regions_connections = 2
        game_solver = StitchesSolver(grid, dots_by_column_row, regions_connections, self.get_solver_engine())
        solution = game_solver.get_solution()
        self.assertEqual(expected_solution, solution)
        other_solution = game_solver.get_other_solution()
        self.assertTrue(other_solution.is_empty())


if __name__ == '__main__':
    unittest.main()
