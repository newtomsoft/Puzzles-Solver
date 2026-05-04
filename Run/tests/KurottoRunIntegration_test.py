import os
import sys
import unittest
from unittest.mock import patch, AsyncMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from Run.PuzzleMainConsole import PuzzleMainConsole
from GridProviders.GridPuzzle.GridPuzzleKurottoGridProvider import GridPuzzleKurottoGridProvider


class KurottoRunIntegrationTest(unittest.IsolatedAsyncioTestCase):
    async def test_kurotto_via_run_console(self):
        url = "https://gridpuzzle.com/kurotto/3j99e"
        html_content = """<!DOCTYPE html>
<html><body>
<div id="puzzle-main" class="box_5">
<div id="c_1" class="g_cell " data-d="0" data-id="1" data-a="#"></div>
<div id="c_2" class="g_cell num_cell" data-d="0" data-id="2" data-a=".">3</div>
<div id="c_3" class="g_cell " data-d="0" data-id="3" data-a="."></div>
<div id="c_4" class="g_cell num_cell" data-d="0" data-id="4" data-a=".">2</div>
<div id="c_5" class="g_cell " data-d="0" data-id="5" data-a="#"></div>
<div id="c_6" class="g_cell " data-d="0" data-id="6" data-a="#"></div>
<div id="c_7" class="g_cell num_cell" data-d="0" data-id="7" data-a=".">3</div>
<div id="c_8" class="g_cell " data-d="0" data-id="8" data-a="."></div>
<div id="c_9" class="g_cell " data-d="0" data-id="9" data-a="#"></div>
<div id="c_10" class="g_cell num_cell" data-d="0" data-id="10" data-a=".">2</div>
<div id="c_11" class="g_cell " data-d="0" data-id="11" data-a="#"></div>
<div id="c_12" class="g_cell " data-d="0" data-id="12" data-a="."></div>
<div id="c_13" class="g_cell " data-d="0" data-id="13" data-a="#"></div>
<div id="c_14" class="g_cell " data-d="0" data-id="14" data-a="."></div>
<div id="c_15" class="g_cell " data-d="0" data-id="15" data-a="."></div>
<div id="c_16" class="g_cell num_cell" data-d="0" data-id="16" data-a=".">7</div>
<div id="c_17" class="g_cell " data-d="0" data-id="17" data-a="#"></div>
<div id="c_18" class="g_cell " data-d="0" data-id="18" data-a="#"></div>
<div id="c_19" class="g_cell num_cell" data-d="0" data-id="19" data-a=".">4</div>
<div id="c_20" class="g_cell " data-d="0" data-id="20" data-a="."></div>
<div id="c_21" class="g_cell " data-d="0" data-id="21" data-a="."></div>
<div id="c_22" class="g_cell num_cell" data-d="0" data-id="22" data-a=".">4</div>
<div id="c_23" class="g_cell " data-d="0" data-id="23" data-a="#"></div>
<div id="c_24" class="g_cell num_cell" data-d="0" data-id="24" data-a=".">5</div>
<div id="c_25" class="g_cell " data-d="0" data-id="25" data-a="#"></div>
</div>
</body></html>
"""
        provider = GridPuzzleKurottoGridProvider()
        grid = provider.get_grid_from_html(html_content)

        with patch('builtins.input', return_value=url), \
             patch.object(GridPuzzleKurottoGridProvider, 'get_grid', new_callable=AsyncMock) as mock_get_grid, \
             patch('GridPlayers.GridPuzzle.GridPuzzleKurottoPlayer.GridPuzzleKurottoPlayer.play', new_callable=AsyncMock) as mock_play:

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
