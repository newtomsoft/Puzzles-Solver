import unittest
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from Puzzles.Kakuro.KakuroMainConsole import KakuroMainConsole


class TestMainFunction(TestCase):
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

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

    @patch('builtins.input', side_effect=["1 | 1 _ 2 | 2"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_wrong_input_size(self, mock_stdout, mock_input):
        KakuroMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn('Error: The grid must be at least 3x3', output)

    @patch('builtins.input', side_effect=[r"0\0 | 19\0 | 19\0 _ 0\19 | 0 | 0 _ 0\19 | 0 | 0"])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('webbrowser.open')
    def test_main_with_wrong_grid(self, mock_browser_open, mock_stdout, mock_input):
        KakuroMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn("No solution found", output)

    @patch('builtins.input', side_effect=[r"0\0 | 4\0 | 6\0 _ 0\3 | 0 | 0 _ 0\7 | 0 | 0"])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('webbrowser.open')
    def test_main_with_grid(self, mock_browser_open, mock_stdout, mock_input):
        KakuroMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn("Solution found", output)
        self.assertIn("•••\n•12\n•34", output)
        mock_browser_open.assert_called_once()
        html_expected = """<table><tr>
<td class='sum-cell'><span class='row'></span><span class='column'></span></td><td class='sum-cell'><span class='row'></span><span class='column'>4</span><svg class="line"><line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/></svg></td><td class='sum-cell'><span class='row'></span><span class='column'>6</span><svg class="line"><line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/></svg></td></tr>
<tr>
<td class='sum-cell'><span class='row'>3</span><span class='column'></span><svg class="line"><line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/></svg></td><td class='number-cell'>1</td><td class='number-cell'>2</td></tr>
<tr>
<td class='sum-cell'><span class='row'>7</span><span class='column'></span><svg class="line"><line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/></svg></td><td class='number-cell'>3</td><td class='number-cell'>4</td></tr>
</table>"""
        with open('solution.html', 'r') as file:
            generated_html = file.read()
            self.assertIn(html_expected, generated_html)

    @patch('builtins.input', side_effect=["https://fr.puzzle-kakuro.com/?pl=d8bc15526eb7413efcace7b97adbd5826727c78d46cee"])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('webbrowser.open')
    def test_main_with_url_invariant_game(self, mock_browser_open, mock_stdout, mock_input):
        KakuroMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn("Solution found", output)
        self.assertIn("•••••••\n••13•71\n•154732\n•37•32•\n••31•62\n•625341\n•24•21•", output)
        mock_browser_open.assert_called_once()
        html_expected = """<table><tr>
<td class='sum-cell'><span class='row'></span><span class='column'></span></td><td class='sum-cell'><span class='row'></span><span class='column'></span></td><td class='sum-cell'><span class='row'></span><span class='column'>22</span><svg class="line"><line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/></svg></td><td class='sum-cell'><span class='row'></span><span class='column'>7</span><svg class="line"><line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/></svg></td><td class='sum-cell'><span class='row'></span><span class='column'></span></td><td class='sum-cell'><span class='row'></span><span class='column'>23</span><svg class="line"><line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/></svg></td><td class='sum-cell'><span class='row'></span><span class='column'>3</span><svg class="line"><line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/></svg></td></tr>
<tr>
<td class='sum-cell'><span class='row'></span><span class='column'></span></td><td class='sum-cell'><span class='row'>4</span><span class='column'>4</span><svg class="line"><line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/></svg></td><td class='number-cell'>1</td><td class='number-cell'>3</td><td class='sum-cell'><span class='row'>8</span><span class='column'>10</span><svg class="line"><line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/></svg></td><td class='number-cell'>7</td><td class='number-cell'>1</td></tr>
<tr>
<td class='sum-cell'><span class='row'>22</span><span class='column'></span><svg class="line"><line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/></svg></td><td class='number-cell'>1</td><td class='number-cell'>5</td><td class='number-cell'>4</td><td class='number-cell'>7</td><td class='number-cell'>3</td><td class='number-cell'>2</td></tr>
<tr>
<td class='sum-cell'><span class='row'>10</span><span class='column'></span><svg class="line"><line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/></svg></td><td class='number-cell'>3</td><td class='number-cell'>7</td><td class='sum-cell'><span class='row'>5</span><span class='column'>6</span><svg class="line"><line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/></svg></td><td class='number-cell'>3</td><td class='number-cell'>2</td><td class='sum-cell'><span class='row'></span><span class='column'>3</span><svg class="line"><line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/></svg></td></tr>\n<tr>\n<td class='sum-cell'><span class='row'></span><span class='column'></span></td><td class='sum-cell'><span class='row'>4</span><span class='column'>8</span><svg class="line"><line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/></svg></td><td class='number-cell'>3</td><td class='number-cell'>1</td><td class='sum-cell'><span class='row'>8</span><span class='column'>5</span><svg class="line"><line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/></svg></td><td class='number-cell'>6</td><td class='number-cell'>2</td></tr>
<tr>
<td class='sum-cell'><span class='row'>21</span><span class='column'></span><svg class="line"><line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/></svg></td><td class='number-cell'>6</td><td class='number-cell'>2</td><td class='number-cell'>5</td><td class='number-cell'>3</td><td class='number-cell'>4</td><td class='number-cell'>1</td></tr>
<tr>
<td class='sum-cell'><span class='row'>6</span><span class='column'></span><svg class="line"><line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/></svg></td><td class='number-cell'>2</td><td class='number-cell'>4</td><td class='sum-cell'><span class='row'>3</span><span class='column'></span><svg class="line"><line x1="0" y1="0" x2="100%" y2="100%" stroke="black"/></svg></td><td class='number-cell'>2</td><td class='number-cell'>1</td><td class='sum-cell'><span class='row'></span><span class='column'></span></td></tr>
</table>"""

        with open('solution.html', 'r') as file:
            generated_html = file.read()
            self.assertIn(html_expected, generated_html)

    @patch('builtins.input', side_effect=["https://fr.puzzle-kakuro.com/?size=0"])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('webbrowser.open')
    def test_main_with_url(self, mock_browser_open, mock_stdout, mock_input):
        KakuroMainConsole.main()
        output = mock_stdout.getvalue()
        self.assertIn("Solution found", output)
        mock_browser_open.assert_called_once()


if __name__ == '__main__':
    unittest.main()
