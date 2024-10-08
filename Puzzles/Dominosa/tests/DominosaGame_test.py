import unittest
from unittest import TestCase

from Grid import Grid
from Puzzles.Dominosa.DominosaGame import DominosaGame


class DominosaGameTests(TestCase):
    def _assert_grid_covered(self, solution, original_grid: Grid):
        cover_grid = [[any((r, c) in dominoes_position for dominoes_position in solution.values()) for c in range(original_grid.columns_number)] for r in range(original_grid.rows_number)]
        self.assertTrue(all(all(row) for row in cover_grid))

    def test_solution_not_min_grid(self):
        grid = Grid([[0, 0], [0, 1]])
        with self.assertRaises(ValueError) as context:
            DominosaGame(grid)
        self.assertEqual("The grid must be at least 2x3", str(context.exception))

    def test_solution_not_r_c_grid(self):
        grid = Grid([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        with self.assertRaises(ValueError) as context:
            DominosaGame(grid)
        self.assertEqual("The grid must be RxC with C = R + 1", str(context.exception))

    def test_solution_values_not_0_1(self):
        grid = Grid([[0, 1, 1], [1, 0, 2]])
        with self.assertRaises(ValueError) as context:
            DominosaGame(grid)
        self.assertEqual("Values on dominoes must be between x and x + 1", str(context.exception))

    def test_solution_values_not_1_2_3(self):
        grid = Grid([[1, 2, 3, 4], [2, 3, 1, 1], [3, 1, 2, 1]])
        with self.assertRaises(ValueError) as context:
            DominosaGame(grid)
        self.assertEqual("Values on dominoes must be between x and x + 2", str(context.exception))

    def test_solution_not_r_c_grid_2(self):
        grid = Grid([[0, 1, 0], [1, 0, 1]])
        solution = DominosaGame(grid).get_solution()
        self.assertEqual({}, solution)

    def test_solution_2x3(self):
        grid = Grid([[0, 1, 1], [1, 0, 0]])

        expected_dominoes_coordinates = {
            (0, 0): {(1, 1), (1, 2)},
            (1, 0): {(0, 0), (1, 0)},
            (1, 1): {(0, 1), (0, 2)},
        }

        solution = DominosaGame(grid).get_solution()
        self._assert_grid_covered(solution, grid)
        self.assertEqual(expected_dominoes_coordinates, solution)

    def test_solution_4x5(self):
        grid = Grid([
            [1, 3, 3, 0, 0],
            [1, 2, 2, 1, 0],
            [3, 0, 1, 2, 2],
            [3, 1, 0, 3, 2]
        ])

        expected_dominoes_coordinates = {
            (0, 0): {(0, 3), (0, 4)},
            (1, 0): {(2, 2), (3, 2)},
            (1, 1): {(0, 0), (1, 0)},
            (2, 0): {(1, 4), (2, 4)},
            (2, 1): {(1, 3), (2, 3)},
            (2, 2): {(1, 1), (1, 2)},
            (3, 0): {(2, 0), (2, 1)},
            (3, 1): {(3, 0), (3, 1)},
            (3, 2): {(3, 3), (3, 4)},
            (3, 3): {(0, 1), (0, 2)}}

        solution = DominosaGame(grid).get_solution()
        self._assert_grid_covered(solution, grid)
        self.assertEqual(expected_dominoes_coordinates, solution)

    def test_solution_4x5_2(self):
        grid = Grid([
            [0, 1, 0, 3, 2],
            [3, 1, 2, 0, 1],
            [1, 3, 0, 0, 2],
            [2, 2, 3, 3, 1]
        ])

        expected_dominoes_coordinates = {
            (0, 0): {(2, 2), (2, 3)},
            (1, 0): {(1, 3), (1, 4)},
            (1, 1): {(0, 1), (1, 1)},
            (2, 0): {(0, 2), (1, 2)},
            (2, 1): {(2, 4), (3, 4)},
            (2, 2): {(3, 0), (3, 1)},
            (3, 0): {(0, 0), (1, 0)},
            (3, 1): {(2, 0), (2, 1)},
            (3, 2): {(0, 3), (0, 4)},
            (3, 3): {(3, 2), (3, 3)},
        }

        solution = DominosaGame(grid).get_solution()
        self._assert_grid_covered(solution, grid)
        self.assertEqual(expected_dominoes_coordinates, solution)

    def test_solution_5x6(self):
        grid = Grid([
            [4, 0, 4, 3, 3, 3],
            [1, 4, 3, 4, 2, 1],
            [3, 4, 2, 0, 4, 0],
            [2, 0, 0, 0, 3, 1],
            [2, 2, 2, 1, 1, 1]
        ])

        expected_dominoes_coordinates = {
            (0, 0): {(3, 1), (3, 2)},
            (1, 0): {(2, 5), (3, 5)},
            (1, 1): {(4, 4), (4, 5)},
            (2, 0): {(2, 2), (2, 3)},
            (2, 1): {(4, 2), (4, 3)},
            (2, 2): {(4, 0), (4, 1)},
            (3, 0): {(3, 3), (3, 4)},
            (3, 1): {(0, 5), (1, 5)},
            (3, 2): {(2, 0), (3, 0)},
            (3, 3): {(0, 3), (0, 4)},
            (4, 0): {(0, 1), (0, 2)},
            (4, 1): {(0, 0), (1, 0)},
            (4, 2): {(1, 4), (2, 4)},
            (4, 3): {(1, 2), (1, 3)},
            (4, 4): {(1, 1), (2, 1)}
        }

        solution = DominosaGame(grid).get_solution()
        self._assert_grid_covered(solution, grid)
        self.assertEqual(expected_dominoes_coordinates, solution)

    def test_solution_6x7(self):
        grid = Grid([
            [3, 1, 2, 1, 4, 4, 0],
            [1, 5, 2, 1, 4, 3, 0],
            [0, 3, 3, 2, 4, 3, 5],
            [2, 3, 5, 2, 1, 5, 1],
            [2, 4, 0, 4, 2, 0, 0],
            [3, 4, 0, 5, 5, 5, 1]
        ])

        expected_dominoes_coordinates = {
            (0, 0): {(4, 2), (5, 2)},
            (1, 0): {(4, 6), (5, 6)},
            (1, 1): {(0, 3), (1, 3)},
            (2, 0): {(4, 4), (4, 5)},
            (2, 1): {(0, 1), (0, 2)},
            (2, 2): {(2, 3), (3, 3)},
            (3, 0): {(2, 0), (2, 1)},
            (3, 1): {(0, 0), (1, 0)},
            (3, 2): {(3, 0), (3, 1)},
            (3, 3): {(1, 5), (2, 5)},
            (4, 0): {(0, 5), (0, 6)},
            (4, 1): {(2, 4), (3, 4)},
            (4, 2): {(4, 0), (4, 1)},
            (4, 3): {(5, 0), (5, 1)},
            (4, 4): {(0, 4), (1, 4)},
            (5, 0): {(1, 6), (2, 6)},
            (5, 1): {(3, 5), (3, 6)},
            (5, 2): {(1, 1), (1, 2)},
            (5, 3): {(2, 2), (3, 2)},
            (5, 4): {(4, 3), (5, 3)},
            (5, 5): {(5, 4), (5, 5)}
        }

        solution = DominosaGame(grid).get_solution()
        self._assert_grid_covered(solution, grid)
        self.assertEqual(expected_dominoes_coordinates, solution)

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

        expected_dominoes_coordinates = {
            (0, 0): {(4, 2), (4, 3)},
            (1, 0): {(2, 0), (3, 0)},
            (1, 1): {(2, 4), (3, 4)},
            (2, 0): {(4, 6), (5, 6)},
            (2, 1): {(5, 2), (6, 2)},
            (2, 2): {(2, 3), (3, 3)},
            (3, 0): {(5, 1), (6, 1)},
            (3, 1): {(3, 6), (3, 7)},
            (3, 2): {(2, 6), (2, 7)},
            (3, 3): {(5, 3), (5, 4)},
            (4, 0): {(6, 3), (6, 4)},
            (4, 1): {(5, 5), (6, 5)},
            (4, 2): {(4, 7), (5, 7)},
            (4, 3): {(1, 2), (1, 3)},
            (4, 4): {(0, 5), (1, 5)},
            (5, 0): {(3, 1), (3, 2)},
            (5, 1): {(6, 6), (6, 7)},
            (5, 2): {(0, 2), (0, 3)},
            (5, 3): {(0, 0), (1, 0)},
            (5, 4): {(4, 0), (4, 1)},
            (5, 5): {(0, 7), (1, 7)},
            (6, 0): {(0, 6), (1, 6)},
            (6, 1): {(0, 4), (1, 4)},
            (6, 2): {(5, 0), (6, 0)},
            (6, 3): {(0, 1), (1, 1)},
            (6, 4): {(2, 1), (2, 2)},
            (6, 5): {(4, 4), (4, 5)},
            (6, 6): {(2, 5), (3, 5)}
        }

        solution = DominosaGame(grid).get_solution()
        self._assert_grid_covered(solution, grid)
        self.assertEqual(expected_dominoes_coordinates, solution)

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

        expected_dominoes_coordinates = {
            (0, 0): {(8, 4), (9, 4)},
            (1, 0): {(9, 2), (9, 3)},
            (1, 1): {(2, 5), (3, 5)},
            (2, 0): {(2, 4), (3, 4)},
            (2, 1): {(3, 0), (3, 1)},
            (2, 2): {(5, 3), (6, 3)},
            (3, 0): {(4, 3), (4, 4)},
            (3, 1): {(1, 0), (1, 1)},
            (3, 2): {(9, 5), (9, 6)},
            (3, 3): {(6, 9), (6, 10)},
            (4, 0): {(2, 0), (2, 1)},
            (4, 1): {(2, 2), (3, 2)},
            (4, 2): {(4, 9), (4, 10)},
            (4, 3): {(8, 0), (9, 0)},
            (4, 4): {(8, 9), (8, 10)},
            (5, 0): {(4, 1), (5, 1)},
            (5, 1): {(6, 4), (6, 5)},
            (5, 2): {(0, 0), (0, 1)},
            (5, 3): {(4, 2), (5, 2)},
            (5, 4): {(3, 7), (3, 8)},
            (5, 5): {(0, 5), (1, 5)},
            (6, 0): {(5, 4), (5, 5)},
            (6, 1): {(1, 9), (1, 10)},
            (6, 2): {(8, 5), (8, 6)},
            (6, 3): {(4, 0), (5, 0)},
            (6, 4): {(8, 2), (8, 3)},
            (6, 5): {(6, 0), (6, 1)},
            (6, 6): {(6, 8), (7, 8)},
            (7, 0): {(8, 8), (9, 8)},
            (7, 1): {(4, 5), (4, 6)},
            (7, 2): {(1, 8), (2, 8)},
            (7, 3): {(1, 7), (2, 7)},
            (7, 4): {(0, 6), (1, 6)},
            (7, 5): {(7, 3), (7, 4)},
            (7, 6): {(0, 4), (1, 4)},
            (7, 7): {(7, 0), (7, 1)},
            (8, 0): {(6, 2), (7, 2)},
            (8, 1): {(9, 9), (9, 10)},
            (8, 2): {(1, 2), (1, 3)},
            (8, 3): {(0, 2), (0, 3)},
            (8, 4): {(5, 6), (6, 6)},
            (8, 5): {(5, 9), (5, 10)},
            (8, 6): {(4, 7), (4, 8)},
            (8, 7): {(8, 1), (9, 1)},
            (8, 8): {(2, 9), (3, 9)},
            (9, 0): {(0, 9), (0, 10)},
            (9, 1): {(7, 9), (7, 10)},
            (9, 2): {(2, 10), (3, 10)},
            (9, 3): {(5, 7), (5, 8)},
            (9, 4): {(7, 5), (7, 6)},
            (9, 5): {(2, 6), (3, 6)},
            (9, 6): {(8, 7), (9, 7)},
            (9, 7): {(0, 7), (0, 8)},
            (9, 8): {(2, 3), (3, 3)},
            (9, 9): {(6, 7), (7, 7)}}

        solution = DominosaGame(grid).get_solution()
        self._assert_grid_covered(solution, grid)
        self.assertEqual(expected_dominoes_coordinates, solution)


if __name__ == '__main__':
    unittest.main()
