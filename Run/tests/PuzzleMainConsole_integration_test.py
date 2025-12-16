import os
import sys
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch

# Add paths for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))  # Root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Run

from GridPlayers.PuzzleMobiles.PuzzleKurodokoPlayer import PuzzleKurodokoPlayer
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from Run.PuzzleMainConsole import PuzzleMainConsole


class PuzzleMainConsoleIntegrationTests(unittest.TestCase):

    @patch('builtins.input', return_value="https://fr.puzzle-kurodoko.com/?size=1")
    @patch('sys.stdout', new_callable=StringIO)
    @patch.object(PuzzleKurodokoPlayer, 'submit_score')
    def test_integration_kurodoko_headless(self, mock_submit_score, mock_stdout, mock_input):
        original_read_config = PlaywrightGridProvider._read_config

        def side_effect_read_config(self_provider):
            original_read_config(self_provider)
            self_provider.headless = False
            print(f"Forced headless mode for test: {self_provider.headless}")

        with patch.object(PlaywrightGridProvider, '_read_config', side_effect=side_effect_read_config, autospec=True):
            try:
                PuzzleMainConsole.main()
            except Exception:
                import traceback
                traceback.print_exc()
                raise

        output = mock_stdout.getvalue()

        # Verify steps
        self.assertIn("Puzzle Solver", output)
        self.assertIn("Enter game url", output)
        self.assertIn("getting grid...", output)
        self.assertIn("Solving...", output)
        self.assertIn("Solution found in", output)

        # Verify Player played
        mock_submit_score.assert_called_once()


if __name__ == '__main__':
    unittest.main()
