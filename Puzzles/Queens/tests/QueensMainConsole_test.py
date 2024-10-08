import unittest
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from PlaywrightGridProvider import PlaywrightGridProvider
from Puzzles.Queens.QueensMainConsole import QueensMainConsole
from utils import clean_ansi_escape_codes


class TestMainFunction(TestCase):
    def setUp(self):
        self.patcher = patch.object(PlaywrightGridProvider, 'get_config')
        self.mock_get_config = self.patcher.start()
        mock_config = {
            'DEFAULT': {
                'email': 'test@example.com',
                'password': 'password123',
                'headless': 'False',
                'user_data_path': r'Chromium\user',
                'extensions_path': r'Chromium\extensions\NoScript\11.4.18_0,Chromium\extensions\Consent-O-Matic\1.0.13_0'
            }
        }
        self.mock_get_config.return_value = mock_config

    def tearDown(self):
        self.patcher.stop()

    @patch('builtins.input', side_effect=["1 1 2 2"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_wrong_input_size(self, mock_stdout, mock_input):
        QueensMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn('Error: The grid must be at least 4x4', output)

    @patch('builtins.input', side_effect=["1 1 1 1 1 2 2 2 2 2 3 3 3 3 3 4 4 4 4 4 5 5 5 5 5 6 6 6 6 6"])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('webbrowser.open')
    def test_main_with_input_not_square_grid(self, mock_browser_open, mock_stdout, mock_input):
        QueensMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn('Warning: grid cropped to be square', output)

    @patch('builtins.input', side_effect=["0 0 0 0 8 2 2 3 4 0 6 6 8 8 8 2 3 4 0 5 6 6 8 3 3 3 4 0 5 8 8 8 8 8 7 4 0 5 5 5 8 7 7 7 4 0 8 8 8 8 8 8 8 4 1 1 4 4 8 4 4 4 4 1 1 4 8 8 8 4 4 4 1 4 4 4 4 4 4 4 4"])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('webbrowser.open')
    def test_main_with_grid(self, mock_browser_open, mock_stdout, mock_input):
        QueensMainConsole.main()
        output = clean_ansi_escape_codes(mock_stdout.getvalue())
        self.assertIn("Solution found", output)
        expected_result = ('                   *       \n'
                           '       *                   \n'
                           '                *          \n'
                           '                      *    \n'
                           '          *                \n'
                           ' *                         \n'
                           '             *             \n'
                           '    *                      \n'
                           '                         * \n')
        self.assertIn(expected_result, output)

    @patch('builtins.input', side_effect=["https://www.linkedin.com/games/queens/"])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('webbrowser.open')
    def test_main_with_url(self, mock_browser_open, mock_stdout, mock_input):
        QueensMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn("Solution found", output)
        mock_browser_open.assert_called_once()
        # content of the solution not tested because changes every day


if __name__ == '__main__':
    unittest.main()
