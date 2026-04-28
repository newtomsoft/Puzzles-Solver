import os
import sys
import unittest
from unittest.mock import patch, AsyncMock

# Ajout des chemins nécessaires
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from Run.PuzzleMainConsole import PuzzleMainConsole
from GridProviders.GridPuzzle.GridPuzzleKnossosGridProvider import GridPuzzleKnossosGridProvider

class KnossosRunIntegrationTest(unittest.IsolatedAsyncioTestCase):
    async def test_knossos_via_run_console(self):
        # On simule l'entrée utilisateur pour l'URL
        url = "https://gridpuzzle.com/knossos/3164k"
        
        # On lit le contenu HTML du sample pour mocker la réponse du provider
        current_dir = os.path.dirname(__file__)
        asset_path = os.path.join(current_dir, "..", "..", "GridProviders", "GridPuzzle", "tests", "assets", "knossos_3164k.html")
        with open(asset_path, "r", encoding='utf-8') as f:
            html_content = f.read()

        # On instancie le provider pour extraire la grille
        provider = GridPuzzleKnossosGridProvider()
        grid = provider.get_grid_from_html(html_content)

        # On patch input pour l'URL
        # On patch get_grid du provider pour ne pas ouvrir de vrai navigateur
        # On patch GridPuzzleKnossosPlayer.play pour ne pas essayer de jouer
        
        with patch('builtins.input', return_value=url), \
             patch.object(GridPuzzleKnossosGridProvider, 'get_grid', new_callable=AsyncMock) as mock_get_grid, \
             patch('GridPlayers.GridPuzzle.GridPuzzleKnossosPlayer.GridPuzzleKnossosPlayer.play', new_callable=AsyncMock) as mock_play:
            
            # mock_get_grid doit retourner (game_data, browser_context, playwright)
            mock_get_grid.return_value = (grid, AsyncMock(), AsyncMock())
            mock_play.return_value = "SUCCESS"

            # On capture la sortie standard pour vérifier les prints
            from io import StringIO
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                await PuzzleMainConsole.main()
                output = mock_stdout.getvalue()

        # Vérifications
        self.assertIn("Puzzle Solver", output)
        self.assertIn("getting grid...", output)
        self.assertIn("Solving...", output)
        self.assertIn("Solution found in", output)
        self.assertIn("Game played successfully", output)
        
        self.assertIn("2 0 0 3 1", output)
        self.assertIn("8 9 9 10 10", output)

if __name__ == '__main__':
    unittest.main()
