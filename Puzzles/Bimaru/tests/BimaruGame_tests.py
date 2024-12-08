import unittest
from unittest import TestCase

from Position import Position
from Puzzles.Bimaru.BimaruGame import BimaruGame
from Utils.Grid import Grid


class BimaruGameTests(TestCase):
    @staticmethod
    def _to_bool(grid: Grid):
        if grid.is_empty():
            return Grid.empty()
        return Grid([[True if grid[Position(r, c)] > 0 else False for c in range(6)] for r in range(6)])

    def test_grid_must_be_square_raises_value_error(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        boats = {'column': [1, 0, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0, 0]}
        boats_number_by_size = {1: 1}
        with self.assertRaises(ValueError) as context:
            BimaruGame((grid, boats, boats_number_by_size))
        self.assertEqual("The grid must be square", str(context.exception))

    def test_grid_must_be_at_least_4x4_raises_value_error(self):
        grid = Grid([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])
        boats = {'column': [1, 0, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0, 0]}
        boats_number_by_size = {1: 1}
        with self.assertRaises(ValueError) as context:
            BimaruGame((grid, boats, boats_number_by_size))
        self.assertEqual("The grid must be at least 6x6", str(context.exception))

    def test_boats_number_by_size_not_filled(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        boats = {'column': [1, 0, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0]}
        boats_number_by_size = {}
        with self.assertRaises(ValueError) as context:
            BimaruGame((grid, boats, boats_number_by_size))
        self.assertEqual("At least one boat must be placed", str(context.exception))

    def test_boats_column_not_compliant(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        boats = {'column': [1, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0, 0]}
        boats_number_by_size = {1: 1}
        with self.assertRaises(ValueError) as context:
            BimaruGame((grid, boats, boats_number_by_size))
        self.assertEqual("Boat cells column must have the same length as the columns number", str(context.exception))

    def test_boats_rows_not_compliant(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        boats = {'column': [1, 0, 0, 0, 0, 0], 'row': [1, 0, 0, 0, 0]}
        boats_number_by_size = {1: 1}
        with self.assertRaises(ValueError) as context:
            BimaruGame((grid, boats, boats_number_by_size))
        self.assertEqual("Boat cells row must have the same length as the rows number", str(context.exception))

    def test_boats_rows_columns_not_equal(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        boats = {'column': [2, 1, 1, 0, 0, 0], 'row': [1, 1, 1, 0, 0, 0]}
        boats_number_by_size = {1: 2, 2: 1}
        with self.assertRaises(ValueError) as context:
            BimaruGame((grid, boats, boats_number_by_size))
        self.assertEqual("The sum of boat cells by row and column must be equal", str(context.exception))

    def test_boats_cell_number_not_compliant(self):
        grid = Grid([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        boats = {'column': [2, 1, 1, 0, 0, 0], 'row': [1, 2, 1, 0, 0, 0]}
        boats_number_by_size = {1: 3, 2: 1}
        with self.assertRaises(ValueError) as context:
            BimaruGame((grid, boats, boats_number_by_size))
        self.assertEqual("The sum of the size of the ships must be equal to the sum of boats cells", str(context.exception))

    def test_solution_with_sums_constraints(self):
        grid = Grid([
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        expected_solution = Grid([
            [6, 0, 6, 0, 6, 0],
            [0, 0, 0, 0, 0, 0],
            [6, 0, 6, 0, 6, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        boats = {'column': [2, 0, 2, 0, 2, 0], 'row': [3, 0, 3, 0, 0, 0]}
        boats_number_by_size = {1: 6}
        solution = BimaruGame((grid, boats, boats_number_by_size))
        self.assertEqual(self._to_bool(expected_solution), self._to_bool(solution.get_solution()))

    def test_solution_with_initials_constraints_0(self):
        grid = Grid([
            [1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        boats = {'column': [1, 1, 0, 0, 0, 0], 'row': [1, 1, 0, 0, 0, 0]}
        boats_number_by_size = {1: 2}
        solution = BimaruGame((grid, boats, boats_number_by_size))
        self.assertEqual(Grid.empty(), solution.get_solution())

    def test_solution_with_initials_constraints_1(self):
        grid = Grid([
            [1, -1, -1, -1, -1, -1],
            [2, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        expected_solution = Grid([
            [1, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        boats = {'column': [2, 0, 0, 0, 0, 0], 'row': [1, 1, 0, 0, 0, 0]}
        boats_number_by_size = {2: 1}
        solution = BimaruGame((grid, boats, boats_number_by_size))
        self.assertEqual(self._to_bool(expected_solution), self._to_bool(solution.get_solution()))

    def test_solution_with_initials_constraints_2(self):
        grid = Grid([
            [1, -1, -1, -1, -1, -1],
            [2, -1, -1, -1, -1, -1],
            [2, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        boats = {'column': [3, 0, 0, 0, 0, 0], 'row': [1, 1, 1, 0, 0, 0]}
        boats_number_by_size = {3: 1}
        solution = BimaruGame((grid, boats, boats_number_by_size))
        self.assertEqual(Grid.empty(), self._to_bool(solution.get_solution()))

    def test_solution_with_initials_constraints_3(self):
        grid = Grid([
            [3, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
        ])
        expected_solution = Grid([
            [3, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        boats = {'column': [1, 1, 0, 0, 0, 0], 'row': [2, 0, 0, 0, 0, 0]}
        boats_number_by_size = {2: 1}
        solution = BimaruGame((grid, boats, boats_number_by_size))
        self.assertEqual(self._to_bool(expected_solution), self._to_bool(solution.get_solution()))


if __name__ == '__main__':
    unittest.main()
