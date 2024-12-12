import unittest
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from Puzzles.Hitori.HitoriMainConsole import HitoriMainConsole


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

    @patch('builtins.input', side_effect=["1 1 1 1"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_wrong_input_should_not_find_solution(self, mock_stdout, mock_input):
        HitoriMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn('No solution found', output)

    @patch('builtins.input', side_effect=["1 1 1 2"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_grid_basic_input(self, mock_stdout, mock_input):
        HitoriMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn('■1\n12', output)

    @patch('builtins.input', side_effect=["1 2 3 1 2 2 2 3 1"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_grid_3x3_binput(self, mock_stdout, mock_input):
        HitoriMainConsole.main()
        output = mock_stdout.getvalue()
        expected_result = '■23\n1■2\n231'
        self.assertIn(expected_result, output)

    @patch('builtins.input', side_effect=["5 1 1 4 5 5 4 3 5 1 2 2 5 2 4 3 2 2 1 5 2 5 4 3 1"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_grid_3x3_binput(self, mock_stdout, mock_input):
        HitoriMainConsole.main()
        output = mock_stdout.getvalue()
        expected_result = '51■4■\n■4351\n2■5■4\n32■15\n■543■'
        self.assertIn(expected_result, output)

    @patch('builtins.input', side_effect=["https://hitoriconquest.com/?puzzle_id=13138"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_url_input(self, mock_stdout, mock_input):
        HitoriMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn("Solution found", output)
        expected_result = '■32■5\n52■41\n■43■2\n2■413\n351■4'
        self.assertIn(expected_result, output)

    @patch('builtins.input', side_effect=["https://hitoriconquest.com/?puzzle_id=9211"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_url_input_8x8(self, mock_stdout, mock_input):
        HitoriMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn("Solution found", output)
        expected_result = '■8■71■62\n632178■4\n8■13■625\n■7■58■3■\n1632■578\n5■4■2■8■\n25■83416\n■18■6■5■'
        self.assertIn(expected_result, output)


if __name__ == '__main__':
    unittest.main()
