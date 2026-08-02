import unittest

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from GridProviders.PuzzLink.PuzzLinkRomaGridProvider import PuzzLinkRomaGridProvider

_ = None


class PuzzLinkRomaGridProviderTests(unittest.TestCase):
    def test_decode_official_fixture(self):
        url = 'https://puzz.link/p?roma/3/3/70og4a322c5'
        arrows_grid, regions_grid = PuzzLinkRomaGridProvider._parse_url(url)

        self.assertEqual(3, arrows_grid.rows_number)
        self.assertEqual(3, arrows_grid.columns_number)
        self.assertEqual(3, regions_grid.rows_number)
        self.assertEqual(3, regions_grid.columns_number)

        expected_arrows = Grid([
            ['R', _, 'L'],
            ['D', 'D', _],
            [_, _, 'G'],
        ])

        expected_regions = Grid([
            [1, 1, 1],
            [2, 3, 1],
            [2, 3, 3],
        ])

        self.assertEqual(expected_arrows, arrows_grid)
        self.assertEqual(expected_regions, regions_grid)

    def test_invalid_url(self):
        with self.assertRaises(ValueError):
            PuzzLinkRomaGridProvider._parse_url('https://puzz.link/p?roma/3/3')


if __name__ == '__main__':
    unittest.main()
