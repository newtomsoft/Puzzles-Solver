import unittest

from Domain.Board.Grid import Grid
from GridProviders.PuzzLink.PuzzLinkContextGridProvider import PuzzLinkContextGridProvider

_ = None


class PuzzLinkContextGridProviderTests(unittest.TestCase):
    def test_decode_url(self):
        url = 'https://puzz.link/p?context/8/8/k1j2i3h2h3n1j3n1h2h2i2j2k'
        grid = PuzzLinkContextGridProvider._parse_url(url)

        self.assertEqual(8, grid.rows_number)
        self.assertEqual(8, grid.columns_number)

        expected = Grid([
            [_, _, _, _, _, 1, _, _],
            [_, _, 2, _, _, _, 3, _],
            [_, 2, _, _, 3, _, _, _],
            [_, _, _, _, _, 1, _, _],
            [_, _, 3, _, _, _, _, _],
            [_, _, _, 1, _, _, 2, _],
            [_, 2, _, _, _, 2, _, _],
            [_, _, 2, _, _, _, _, _],
        ])

        self.assertEqual(expected, grid)

if __name__ == '__main__':
    unittest.main()
