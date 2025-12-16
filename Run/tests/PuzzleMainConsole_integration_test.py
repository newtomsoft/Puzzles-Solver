import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch

# Add paths for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))  # Root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Run

from GridPlayers.PuzzleMobiles.PuzzleKurodokoPlayer import PuzzleKurodokoPlayer
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from Run.PuzzleMainConsole import PuzzleMainConsole


class PuzzleMainConsoleIntegrationTests(unittest.TestCase):

    @patch('GridPlayers.PuzzleMobiles.PuzzleKurodokoPlayer.sleep', return_value=None)  # Mock sleep to speed up test execution
    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', return_value="https://fr.puzzle-kurodoko.com/?size=1")
    def test_integration_kurodoko_headless(self, mock_input, mock_stdout, mock_sleep):
        # Ensure mock parameters are used to satisfy IDE warnings (they're needed for the @patch decorators)
        assert mock_input is not None
        assert mock_sleep is not None
        original_read_config = PlaywrightGridProvider._read_config

        def side_effect_read_config(self_provider):
            original_read_config(self_provider)
            self_provider.headless = True
            print(f"Forced headless mode for test: {self_provider.headless}")

        with patch.object(PlaywrightGridProvider, '_read_config', side_effect=side_effect_read_config, autospec=True):
            try:
                PuzzleMainConsole.main()
            except Exception:
                import traceback
                traceback.print_exc()
                raise

        output = mock_stdout.getvalue()

        self.assertIn("Puzzle Solver", output)
        self.assertIn("Enter game url", output)
        self.assertIn("getting grid...", output)
        self.assertIn("Solving...", output)
        self.assertIn("Solution found in", output)


if __name__ == '__main__':
    unittest.main()
