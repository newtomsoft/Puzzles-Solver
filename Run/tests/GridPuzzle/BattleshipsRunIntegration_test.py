import os
import sys
import unittest
from unittest.mock import patch, AsyncMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from Run.PuzzleMainConsole import PuzzleMainConsole
from GridProviders.GridPuzzle.GridPuzzleBattleshipsGridProvider import GridPuzzleBattleshipsGridProvider
from Run.Games import BattleshipsConfig


class BattleshipsRunIntegrationTest(unittest.IsolatedAsyncioTestCase):
    async def test_battleships_via_run_console(self):
        BattleshipsConfig.register()
        url = "https://gridpuzzle.com/battleships/21479"
        current_dir = os.path.dirname(__file__)
        asset_path = os.path.join(current_dir, "../..", "..", "GridProviders", "GridPuzzle", "tests", "assets", "battleships_sample.html")
        with open(asset_path, "r", encoding='utf-8') as f:
            html_content = f.read()

        provider = GridPuzzleBattleshipsGridProvider()
        result = provider.get_grid_from_html(html_content)

        with patch('builtins.input', return_value=url), \
             patch.object(GridPuzzleBattleshipsGridProvider, 'get_grid', new_callable=AsyncMock) as mock_get_grid, \
             patch('GridPlayers.GridPuzzle.GridPuzzleBattleshipsPlayer.GridPuzzleBattleshipsPlayer.play', new_callable=AsyncMock) as mock_play:

            mock_get_grid.return_value = (result, AsyncMock(), AsyncMock())
            mock_play.return_value = "SUCCESS"

            from io import StringIO
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                await PuzzleMainConsole.main()
                output = mock_stdout.getvalue()

        self.assertIn("Puzzle Solver", output)
        self.assertIn("getting grid...", output)
        self.assertIn("Solving...", output)
        self.assertIn("Solution found in", output)
        self.assertIn("Game played successfully", output)


if __name__ == '__main__':
    unittest.main()
