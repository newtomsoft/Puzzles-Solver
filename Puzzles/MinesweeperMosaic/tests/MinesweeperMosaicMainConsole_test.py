import unittest
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from GridProviders.ScrapingGridProvider import PlaywrightGridProvider

from Puzzles.MinesweeperMosaic.MinesweeperMosaicMainConsole import MinesweeperMosaicMainConsole


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

    @patch('builtins.input', side_effect=["0 1 0 0"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_wrong_input_should_not_find_solution(self, mock_stdout, mock_input):
        MinesweeperMosaicMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn('No solution found', output)

    @patch('builtins.input', side_effect=["-1 -1 1 0 -1 -1 -1 -1 0"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_grid_basic_input(self, mock_stdout, mock_input):
        MinesweeperMosaicMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn('  ■\n   \n   \n', output)
        html_expected = ("<html><head><style>table {border-collapse: collapse;} td {border: 1px solid black; width: 20px; height: 20px; text-align: center;}</style></head><body><table><tr><td style='background-color: white; color: black;'> </td><td "
                         "style='background-color: white; color: black;'> </td><td style='background-color: black; color: white;'>1</td></tr><tr><td style='background-color: white; color: black;'>0</td><td style='background-color: white; color: black;'> </td><td "
                         "style='background-color: white; color: black;'> </td></tr><tr><td style='background-color: white; color: black;'> </td><td style='background-color: white; color: black;'> </td><td style='background-color: white; color: "
                         "black;'>0</td></tr></table></body></html>")
        with open('solution.html', 'r') as file:
            generated_html = file.read()
            self.assertIn(html_expected, generated_html)

    @patch('builtins.input', side_effect=["4 -1 -1 2 -1 -1 -1 2 -1 -1 -1 -1 1 -1 3 4 -1 -1 2 -1 -1 -1 -1 -1 -1"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_grid_4x4_input(self, mock_stdout, mock_input):
        MinesweeperMosaicMainConsole.main()
        output = mock_stdout.getvalue()
        expected_result = '■■  ■\n■■  ■\n■   ■\n■   ■\n■■   \n'
        self.assertIn(expected_result, output)
        html_expected = ("<table><tr><td style='background-color: black; color: white;'>4</td><td style='background-color: black; color: white;'> </td><td style='background-color: white; color: black;'> </td><td style='background-color: white; color: black;'>2</td><td "
                         "style='background-color: black; color: white;'> </td></tr><tr><td style='background-color: black; color: white;'> </td><td style='background-color: black; color: white;'> </td><td style='background-color: white; color: black;'>2</td><td "
                         "style='background-color: white; color: black;'> </td><td style='background-color: black; color: white;'> </td></tr><tr><td style='background-color: black; color: white;'> </td><td style='background-color: white; color: black;'> </td><td "
                         "style='background-color: white; color: black;'>1</td><td style='background-color: white; color: black;'> </td><td style='background-color: black; color: white;'>3</td></tr><tr><td style='background-color: black; color: white;'>4</td><td "
                         "style='background-color: white; color: black;'> </td><td style='background-color: white; color: black;'> </td><td style='background-color: white; color: black;'>2</td><td style='background-color: black; color: white;'> </td></tr><tr><td "
                         "style='background-color: black; color: white;'> </td><td style='background-color: black; color: white;'> </td><td style='background-color: white; color: black;'> </td><td style='background-color: white; color: black;'> </td><td "
                         "style='background-color: white; color: black;'> </td></tr></table>")
        with open('solution.html', 'r') as file:
            generated_html = file.read()
            self.assertIn(html_expected, generated_html)

    @patch('builtins.input', side_effect=["https://www.puzzle-minesweeper.com/mosaic-5x5-easy/"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_url_input_5x5_easy(self, mock_stdout, mock_input):
        MinesweeperMosaicMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn("Solution found", output)
        # content of the solution not tested because changes every time

    @patch('builtins.input', side_effect=["https://www.puzzle-minesweeper.com/mosaic-7x7-easy/"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_url_input_7x7_easy(self, mock_stdout, mock_input):
        MinesweeperMosaicMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn("Solution found", output)
        # content of the solution not tested because changes every time

    @patch('builtins.input', side_effect=["https://www.puzzle-minesweeper.com/mosaic-10x10-easy/"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_url_input_10x10_easy(self, mock_stdout, mock_input):
        MinesweeperMosaicMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn("Solution found", output)
        # content of the solution not tested because changes every time

    @patch('builtins.input', side_effect=["https://www.puzzle-minesweeper.com/mosaic-15x15-easy/"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_url_input_15x15_easy(self, mock_stdout, mock_input):
        MinesweeperMosaicMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn("Solution found", output)
        # content of the solution not tested because changes every time

    @patch('builtins.input', side_effect=["https://www.puzzle-minesweeper.com/mosaic-20x20-easy/"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_url_input_20x20_easy(self, mock_stdout, mock_input):
        MinesweeperMosaicMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn("Solution found", output)
        # content of the solution not tested because changes every time

    @patch('builtins.input', side_effect=["https://www.puzzle-minesweeper.com/mosaic-5x5-hard/"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_url_input_5x5_hard(self, mock_stdout, mock_input):
        MinesweeperMosaicMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn("Solution found", output)
        # content of the solution not tested because changes every time

    @patch('builtins.input', side_effect=["https://www.puzzle-minesweeper.com/mosaic-7x7-hard/"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_url_input_7x7_hard(self, mock_stdout, mock_input):
        MinesweeperMosaicMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn("Solution found", output)
        # content of the solution not tested because changes every time

    @patch('builtins.input', side_effect=["https://www.puzzle-minesweeper.com/mosaic-10x10-hard/"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_url_input_10x10_hard(self, mock_stdout, mock_input):
        MinesweeperMosaicMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn("Solution found", output)
        # content of the solution not tested because changes every time

    @patch('builtins.input', side_effect=["https://www.puzzle-minesweeper.com/mosaic-15x15-hard/"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_url_input_15x15_hard(self, mock_stdout, mock_input):
        MinesweeperMosaicMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn("Solution found", output)
        # content of the solution not tested because changes every time

    @patch('builtins.input', side_effect=["https://www.puzzle-minesweeper.com/mosaic-20x20-hard/"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_url_input_20x20_hard(self, mock_stdout, mock_input):
        MinesweeperMosaicMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn("Solution found", output)
        # content of the solution not tested because changes every time


if __name__ == '__main__':
    unittest.main()
