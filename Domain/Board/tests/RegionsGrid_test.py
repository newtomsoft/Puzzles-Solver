import unittest

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.RegionsGrid import RegionsGrid


class RegionsGridTests(unittest.TestCase):
    def test_no_openings_each_cell_is_its_own_region(self):
        openings_grid = Grid([
            [set(), set()],
            [set(), set()],
        ])

        regions = RegionsGrid.from_opened_grid(openings_grid)

        expected = Grid([
            [1, 2],
            [3, 4],
        ])
        self.assertEqual(expected, regions)

    def test_two_regions_in_a_row(self):
        openings_grid = Grid([
            [{Direction.right()}, {Direction.left()}, set()],
        ])

        regions = RegionsGrid.from_opened_grid(openings_grid)

        expected = Grid([
            [1, 1, 2],
        ])
        self.assertEqual(expected, regions)

    def test_2x2_in_3x3_top_left(self):
        openings_grid = Grid([
            [{Direction.right(), Direction.down()}, {Direction.left(), Direction.down()}, {Direction.down()}],
            [{Direction.up(), Direction.right()}, {Direction.left(), Direction.up()}, {Direction.up(), Direction.down()}],
            [{Direction.right()}, {Direction.left(), Direction.right()}, {Direction.left(), Direction.up()}],
        ])

        regions = RegionsGrid.from_opened_grid(openings_grid)

        expected = Grid([
            [1, 1, 2],
            [1, 1, 2],
            [2, 2, 2],
        ])
        self.assertEqual(expected, regions)

    def test_2x2_in_3x3_top_right(self):
        openings_grid = Grid([
            [{Direction.down()}, {Direction.right(), Direction.down()}, {Direction.left(), Direction.down()}],
            [{Direction.up(), Direction.down()}, {Direction.right(), Direction.up()}, {Direction.up(), Direction.left()}],
            [{Direction.right(), Direction.up()}, {Direction.left(), Direction.right()}, {Direction.left()}],
        ])
        regions = RegionsGrid.from_opened_grid(openings_grid)

        expected = Grid([
            [1, 2, 2],
            [1, 2, 2],
            [1, 1, 1],
        ])
        self.assertEqual(expected, regions)

    def test_2x2_in_3x3_bottom_right(self):
        openings_grid = Grid([
            [{Direction.right(), Direction.down()}, {Direction.left(), Direction.right()}, {Direction.left()}],
            [{Direction.up(), Direction.down()}, {Direction.right(), Direction.down()}, {Direction.left(), Direction.down()}],
            [{Direction.up()}, {Direction.up(), Direction.right()}, {Direction.left(), Direction.up()}],
        ])
        regions = RegionsGrid.from_opened_grid(openings_grid)

        expected = Grid([
            [1, 1, 1],
            [1, 2, 2],
            [1, 2, 2]
        ])

        self.assertEqual(expected, regions)


if __name__ == '__main__':
    unittest.main()
