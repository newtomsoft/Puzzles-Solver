import unittest
from unittest.mock import patch, AsyncMock
import os
import re

class GridPuzzleProviderTestBase(unittest.IsolatedAsyncioTestCase):
    async def get_html_content(self, asset_filename):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "assets", asset_filename)
        with open(file_path, "r", encoding='utf-8') as f:
            return f.read()

    def assert_grid_equals(self, expected, actual):
        if isinstance(actual, tuple):
            actual = actual[0]
            
        if isinstance(actual, list) and len(actual) > 0 and isinstance(actual[0], list):
            actual_str = "\n".join([" ".join([str(item) if item is not None else 'None' for item in row]) for row in actual])
        else:
            actual_str = str(actual).strip()
            
        expected_str = str(expected).strip()
            
        actual_str = "\n".join([line.strip() for line in actual_str.splitlines() if line.strip()])
        expected_str = "\n".join([line.strip() for line in expected_str.splitlines() if line.strip()])
        
        actual_str = actual_str.replace(' · ', ' None ').replace('·', 'None')
        expected_str = expected_str.replace(' · ', ' None ').replace('·', 'None')
        
        actual_str = re.sub(r' +', ' ', actual_str)
        expected_str = re.sub(r' +', ' ', expected_str)

        if actual_str != expected_str:
            # Tentative de comparaison sur les valeurs numériques uniquement si c'est du texte
            # Utile pour les grilles avec des styles de bordures différents
            actual_values = re.sub(r'[^a-zA-Z0-9\s-]', 'None', actual_str)
            actual_values = re.sub(r' +', ' ', actual_values).strip()
            
            expected_values = re.sub(r'[^a-zA-Z0-9\s-]', 'None', expected_str)
            expected_values = re.sub(r' +', ' ', expected_values).strip()
            
            if actual_values == expected_values:
                return

            print(f"\nACTUAL:\n{actual_str}")
            print(f"\nEXPECTED:\n{expected_str}")
            
        self.assertEqual(expected_str, actual_str)

    async def run_scrap_test(self, provider_class, asset_filename, method_name='scrap_grid'):
        html_content = await self.get_html_content(asset_filename)
        provider = provider_class()
        
        # On patche get_html pour que l'appel dans scrap_grid ne fasse rien de réseau
        # On patche screen_size pour éviter l'initialisation de tkinter qui peut aussi poser pb en CI
        with patch.object(provider_class, 'get_html', new_callable=AsyncMock) as mock_get_html, \
             patch('GridProviders.PlaywrightGridProvider.PlaywrightGridProvider.screen_size', return_value=(1920, 1080)):
            
            mock_get_html.return_value = html_content
            # On appelle scrap_grid ou scrap_grid_left_up selon le cas
            # Note: on passe None pour le browser car get_html est mocké
            method = getattr(provider, method_name)
            result = await method(None, 'https://dummy.url')
        
        self.assertIsNotNone(result)
        if not result:
            self.fail(f"Provider for {provider_class.__name__} returned empty/false result: {result}")
        return result
