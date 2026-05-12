import unittest

from Domain.Board.Grid import Grid
from GridProviders.PuzzLink.PuzzLinkAyeheyaGridProvider import PuzzLinkAyeheyaGridProvider

_ = None


class PuzzLinkAyeheyaGridProviderTests(unittest.IsolatedAsyncioTestCase):
    async def test_get_grid(self):
        url = 'https://puzz.link/p?ayeheya/11/11/j7j1j1h1hi0i0i0i0papap0v003o03vvs000003vu000g3q3g3j'
        provider = PuzzLinkAyeheyaGridProvider()
        game_data, browser_context, playwright = await provider.get_grid(url)
        try:
            grid, regions = game_data

            self.assertEqual(11, grid.rows_number)
            self.assertEqual(11, grid.columns_number)
            self.assertEqual(11, regions.rows_number)
            self.assertEqual(11, regions.columns_number)

            expected_numbers = Grid([
                [_, 3, _, _, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, 3, _, _, _, _],
                [_, _, _, _, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, 3, _, _, _],
                [_, _, _, _, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _, _, _, _],
            ])

            expected_regions = Grid([
                [0, 1, 1, 1, 2, 3, 3, 3, 4, 5, 6],
                [0, 1, 1, 1, 2, 7, 7, 7, 7, 7, 6],
                [0, 1, 1, 1, 2, 7, 7, 7, 7, 7, 6],
                [0, 8, 8, 8, 8, 7, 7, 7, 7, 7, 6],
                [0, 8, 8, 8, 8, 9, 10, 10, 10, 11, 11],
                [12, 12, 12, 12, 12, 12, 13, 13, 13, 11, 11],
                [12, 12, 12, 12, 12, 12, 13, 13, 13, 11, 11],
                [12, 12, 12, 12, 12, 12, 13, 13, 13, 11, 11],
                [12, 12, 12, 12, 12, 12, 14, 15, 15, 15, 16],
                [17, 17, 18, 18, 19, 19, 14, 15, 15, 15, 16],
                [17, 17, 18, 18, 19, 19, 14, 15, 15, 15, 16],
            ])

            self.assertEqual(expected_numbers, grid)
            self.assertEqual(expected_regions, regions)
        finally:
            if browser_context is not None:
                await browser_context.close()
            if playwright is not None:
                await playwright.stop()


if __name__ == '__main__':
    unittest.main()
