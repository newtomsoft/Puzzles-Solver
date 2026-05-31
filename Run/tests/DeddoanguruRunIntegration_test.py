import os
import sys
import unittest
from unittest.mock import patch, AsyncMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from Run.PuzzleMainConsole import PuzzleMainConsole
from GridProviders.GridPuzzle.GridPuzzleDeddoanguruGridProvider import GridPuzzleDeddoanguruGridProvider
from PuzzleSolver.Board.Grid import Grid


class DeddoanguruRunIntegrationTest(unittest.IsolatedAsyncioTestCase):
    async def test_deddoanguru_via_run_console(self):
        url = "https://gridpuzzle.com/deddoanguru/3e09k"
        html_content = """<html><body><script>
gpl.Size = 4;
gpl.pq = "|3|4|||||||||||1|0|";
gpl.a_r_data = gpl.str2obj("0100100010101110");
gpl.a_b_data = gpl.str2obj("0100011000100000");
gpl.hid = "3e09k";
gpl.init();
</script></body></html>"""
        provider = GridPuzzleDeddoanguruGridProvider()
        grid = provider.get_grid_from_html(html_content)

        with patch('builtins.input', return_value=url), \
             patch.object(GridPuzzleDeddoanguruGridProvider, 'get_grid', new_callable=AsyncMock) as mock_get_grid, \
             patch('GridPlayers.GridPuzzle.GridPuzzleDeddoanguruPlayer.GridPuzzleDeddoanguruPlayer.play', new_callable=AsyncMock) as mock_play:

            mock_get_grid.return_value = (grid, AsyncMock(), AsyncMock())
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
