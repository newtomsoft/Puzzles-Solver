import os
import sys
import unittest
from unittest.mock import patch, AsyncMock

# Ajout des chemins nécessaires
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from Run.PuzzleMainConsole import PuzzleMainConsole
from GridProviders.GridPuzzle.GridPuzzleArofuroGridProvider import GridPuzzleArofuroGridProvider

class ArofuroRunIntegrationTest(unittest.IsolatedAsyncioTestCase):
    async def test_arofuro_via_run_console(self):
        # On simule l'entrée utilisateur pour l'URL
        url = "https://gridpuzzle.com/arofuro/375gk"
        
        # On lit le contenu HTML du sample pour mocker la réponse du provider
        current_dir = os.path.dirname(__file__)
        asset_path = os.path.join(current_dir, "../..", "..", "GridProviders", "GridPuzzle", "tests", "assets", "arofuro_sample.html")
        with open(asset_path, "r", encoding='utf-8') as f:
            html_content = f.read()

        # On instancie le provider pour extraire la grille
        provider = GridPuzzleArofuroGridProvider()
        grid = provider.get_grid_from_html(html_content)

        # On patch input pour l'URL
        # On patch get_grid du provider pour ne pas ouvrir de vrai navigateur
        # On patch GridPuzzleArofuroPlayer.play pour ne pas essayer de jouer (ou on vérifie juste le solver)
        
        with patch('builtins.input', return_value=url), \
             patch.object(GridPuzzleArofuroGridProvider, 'get_grid', new_callable=AsyncMock) as mock_get_grid, \
             patch('GridPlayers.GridPuzzle.GridPuzzleArofuroPlayer.GridPuzzleArofuroPlayer.play', new_callable=AsyncMock) as mock_play:
            
            # mock_get_grid doit retourner (game_data, browser_context, playwright)
            mock_get_grid.return_value = (grid, AsyncMock(), AsyncMock())
            mock_play.return_value = "SUCCESS" # Simule PlayStatus.SUCCESS (ou n'importe quelle valeur non nulle)

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
        
        # Vérification de la grille de solution (partie de l'output)
        # 0 4 3 0
        # 0 3 1 0
        # 3 2 4 2
        # 0 4 1 0
        self.assertIn("0 4 3 0", output)
        self.assertIn("0 3 1 0", output)

if __name__ == '__main__':
    unittest.main()
