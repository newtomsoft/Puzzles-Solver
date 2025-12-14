import unittest
from unittest import TestCase

from Domain.Board.SlantGrid import SlantGrid
from Domain.Puzzles.utils import positions


class GridTest(TestCase):
    def test_slant_from_slant_str(self):
        slant_grid_str = (
            '╱╲\n'
            '╲╱\n'
        )

        expected_slant_grid = SlantGrid([
            [False, True],
            [True, False],
        ])

        self.assertEqual(expected_slant_grid, SlantGrid.from_slant_str(slant_grid_str))

    def test_minimal_no_loop(self):
        grid = SlantGrid.from_slant_str(
            '╲╱\n'
            '╱╲\n'
        )

        self.assertEqual(0, len(grid.get_all_loops()))

    def test_minimal_loop(self):
        grid = SlantGrid.from_slant_str(
            '╱╲\n'
            '╲╱\n'
        )

        expected_loops = positions([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])

        loops = grid.get_all_loops()
        self.assertEqual(1, len(loops))
        self.assertEqual(expected_loops, loops[0])

    def test_double_loop(self):
        grid = SlantGrid.from_slant_str(
            '╱╲╱╲\n'
            '╲╱╲╱\n'
        )

        expected_loops = [
            positions([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]),
            positions([(0, 2), (1, 2), (1, 3), (0, 3), (0, 2)])
        ]

        loops = grid.get_all_loops()
        self.assertEqual(2, len(loops))
        self.assertEqual(expected_loops, loops)

    def test_loop_inside_other(self):
        grid = SlantGrid.from_slant_str(
            '·╱╲·\n'
            '╱╱╲╲\n'
            '╲╲╱╱\n'
            '·╲╱·\n'
        )

        expected_loops = [
            positions([(1, 1), (2, 1), (2, 2), (1, 2), (1, 1)]),
            positions([(0, 1), (1, 0), (2, 0), (3, 1), (3, 2), (2, 3), (1, 3), (0, 2), (0, 1)])
        ]

        loops = grid.get_all_loops()
        self.assertEqual(2, len(loops))
        self.assertEqual(expected_loops, loops)


if __name__ == '__main__':
    unittest.main()
