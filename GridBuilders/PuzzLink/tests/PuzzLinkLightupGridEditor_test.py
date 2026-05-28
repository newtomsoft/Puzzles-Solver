import unittest

from GridBuilders.PuzzLink.PuzzLinkLightupGridEditor import PuzzLinkLightupGridEditor


class PuzzLinkLightupGridEditorTests(unittest.TestCase):
    def test_empty_puzzle(self):
        data_game = {
            'rows_number': 7,
            'columns_number': 7,
            'black_cells': set(),
            'number_constraints': {},
        }
        editor = PuzzLinkLightupGridEditor(data_game)
        url = editor.get_url()
        expected = 'https://puzz.link/p?akari/7/7/zzo'
        self.assertEqual(expected, url)

    def test_puzzle_with_clues(self):
        data_game = {
            'rows_number': 7,
            'columns_number': 7,
            'black_cells': {(0, 4), (1, 1), (1, 5), (2, 0), (3, 3), (5, 5)},
            'number_constraints': {(0, 4): 1, (1, 1): 1, (1, 5): 3, (2, 0): 2, (3, 3): 2, (5, 5): 2},
        }
        editor = PuzzLinkLightupGridEditor(data_game)
        url = editor.get_url()
        self.assertEqual('https://puzz.link/p?akari/7/7/jbgbg8cmcscl', url)

    def test_unnumbered_black_cells_are_skipped(self):
        data_game = {
            'rows_number': 4,
            'columns_number': 4,
            'black_cells': {(0, 0), (1, 1), (2, 2), (3, 3)},
            'number_constraints': {},
        }
        editor = PuzzLinkLightupGridEditor(data_game)
        url = editor.get_url()
        self.assertEqual('https://puzz.link/p?akari/4/4/v', url)

    def test_string_keys_in_number_constraints(self):
        data_game = {
            'rows_number': 5,
            'columns_number': 5,
            'black_cells': set(),
            'number_constraints': {'(1, 2)': 2, '(3, 4)': 0},
        }
        editor = PuzzLinkLightupGridEditor(data_game)
        url = editor.get_url()
        self.assertIn('akari/5/5/', url)

    def test_roundtrip(self):
        data_game = {
            'rows_number': 7,
            'columns_number': 7,
            'black_cells': {(0, 4), (1, 1), (1, 5), (2, 0), (3, 3), (4, 6), (5, 1), (5, 5), (6, 2)},
            'number_constraints': {(0, 4): 1, (1, 1): 1, (1, 5): 3, (2, 0): 2, (3, 3): 2, (5, 5): 2},
        }
        editor = PuzzLinkLightupGridEditor(data_game)
        url = editor.get_url()

        decoded = self._decode_url(url)
        for (r, c), expected_val in data_game['number_constraints'].items():
            self.assertEqual(expected_val, decoded[r * 7 + c], f"Mismatch at ({r}, {c})")

    @staticmethod
    def _decode_url(url: str) -> list[int]:
        import urllib.parse
        parsed = urllib.parse.urlparse(url)
        segments = parsed.query.split('/')
        cols = int(segments[1])
        rows = int(segments[2])
        body = segments[3]
        return PuzzLinkLightupGridEditorTests._decode4cell(body, cols, rows)

    @staticmethod
    def _decode4cell(body: str, cols: int, rows: int) -> list[int]:
        cells = [-1] * (rows * cols)
        a, b = 0, 0
        while b < len(body) and a < rows * cols:
            f = body[b]
            if '0' <= f <= '4':
                cells[a] = int(f, 36)
                a += 1
            elif '5' <= f <= '9':
                cells[a] = int(f, 36) - 5
                a += 2
            elif 'a' <= f <= 'e':
                cells[a] = int(f, 36) - 10
                a += 3
            elif 'g' <= f <= 'z':
                a += int(f, 36) - 15
            elif f == '.':
                cells[a] = -2
                a += 1
            else:
                a += 1
            b += 1
        return cells


if __name__ == '__main__':
    unittest.main()
