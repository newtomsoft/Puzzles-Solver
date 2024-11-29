import unittest
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from PlaywrightGridProvider import PlaywrightGridProvider
from Puzzles.Norinori.NorinoriMainConsole import NorinoriMainConsole
from utils import clean_ansi_escape_codes


class TestMainFunction(TestCase):
    def setUp(self):
        self.patcher = patch.object(PlaywrightGridProvider, 'get_config')
        self.mock_get_config = self.patcher.start()
        mock_config = {
            'DEFAULT': {
                'email': 'test@example.com',
                'password': 'password123',
                'headless': 'True',
                'user_data_path': r'Chromium\user',
                'extensions_path': r'Chromium\extensions\NoScript\11.4.18_0,Chromium\extensions\Consent-O-Matic\1.0.13_0'
            }
        }
        self.mock_get_config.return_value = mock_config

    def tearDown(self):
        self.patcher.stop()

    @patch('builtins.input', side_effect=["1 1 1 1 1 2 2 2 2 2 3 3 3 3 3 4 4 4 4 4 5 5 5 5 5"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_wrong_input_size(self, mock_stdout, mock_input):
        NorinoriMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn('Error: The grid must be at least 6x6', output)

    @patch('builtins.input', side_effect=["1 1 1 1 1 2 2 2 2 2 3 3 3 3 3 4 4 4 4 4 5 5 5 5 5 6 6 6 6 6"])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('webbrowser.open')
    def test_main_with_input_not_square_grid(self, mock_browser_open, mock_stdout, mock_input):
        NorinoriMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn('Warning: grid cropped to be square', output)

    @patch('builtins.input', side_effect=["0 0 1 1 2 1 3 4 1 1 2 1 3 4 4 1 1 1 3 4 4 4 7 7 4 4 6 6 7 7 4 5 5 6 6 7"])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('webbrowser.open')
    def test_main_with_grid(self, mock_browser_open, mock_stdout, mock_input):
        NorinoriMainConsole.main()
        output = mock_stdout.getvalue()
        cleaned_output = clean_ansi_escape_codes(output)
        self.assertIn("Solution found", output)
        expected_result = ' ■  ■        ■    \n       ■     ■    \n ■     ■        ■ \n ■        ■     ■ \n          ■       \n    ■  ■     ■  ■ \n'
        self.assertIn(expected_result, cleaned_output)

    @patch('builtins.input', side_effect=["https://fr.puzzle-norinori.com/"])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('webbrowser.open')
    def test_main_with_url(self, mock_browser_open, mock_stdout, mock_input):
        NorinoriMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn("Solution found", output)
        mock_browser_open.assert_called_once()
        # content of the solution not tested because changes every time


if __name__ == '__main__':
    unittest.main()
