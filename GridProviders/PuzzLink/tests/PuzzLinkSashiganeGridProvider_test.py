import unittest

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from GridProviders.PuzzLink.PuzzLinkSashiganeGridProvider import PuzzLinkSashiganeGridProvider

_ = None


class PuzzLinkSashiganeGridProviderTests(unittest.TestCase):
    def test_decode_official_fixture(self):
        url = 'https://puzz.link/p?sashigane/5/5/jm.o3khkgojm4'
        grid = PuzzLinkSashiganeGridProvider._parse_url(url)

        self.assertEqual(5, grid.rows_number)
        self.assertEqual(5, grid.columns_number)

        expected = Grid([
            [Direction.right(), _, _, _, 0],
            [_, _, _, _, _],
            [3, _, Direction.down(), _, Direction.up()],
            [_, _, _, _, _],
            [Direction.right(), _, _, _, 4],
        ])

        self.assertEqual(expected, grid)

    def test_decode_numbers_and_skips(self):
        url = 'https://puzz.link/p?sashigane/4/4/-10p-64gk.ni'
        grid = PuzzLinkSashiganeGridProvider._parse_url(url)

        expected = Grid([
            [16, _, _, _],
            [_, _, _, 100],
            [Direction.up(), _, 0, _],
            [_, _, _, Direction.left()],
        ])

        self.assertEqual(expected, grid)

    def test_decode_outside_cells(self):
        url = 'https://puzz.link/p?sashigane/3/3/g@kk3'
        grid = PuzzLinkSashiganeGridProvider._parse_url(url)

        expected = Grid([
            [Direction.up(), '#', _],
            [_, 3, _],
            [_, _, _],
        ])

        self.assertEqual(expected, grid)

    def test_invalid_url(self):
        with self.assertRaises(ValueError):
            PuzzLinkSashiganeGridProvider._parse_url('https://puzz.link/p?sashigane/5')


if __name__ == '__main__':
    unittest.main()
