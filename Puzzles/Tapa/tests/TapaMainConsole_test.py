import unittest
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from PlaywrightGridProvider import PlaywrightGridProvider
from Puzzles.Tapa.TapaMainConsole import TapaMainConsole


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

    @patch('builtins.input', side_effect=["https://fr.puzzle-tapa.com/", "n"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_url_puzzles_mobile_daily(self, mock_stdout, mock_input):
        TapaMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn("Solution found", output)
        # content of the solution not tested because changes every time


if __name__ == '__main__':
    unittest.main()
