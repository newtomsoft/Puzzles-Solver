import os
import sys
import unittest
from unittest.mock import AsyncMock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from Run.GameComponentFactory import GameComponentFactory
from Run.GameRegistry import GameRegistry
from GridProviders.PuzzLink.PuzzLinkAyeheyaGridProvider import PuzzLinkAyeheyaGridProvider
from GridProviders.PuzzLink.PuzzLinkRomaGridProvider import PuzzLinkRomaGridProvider


class GameRegistryNormalizationTests(unittest.TestCase):
    def test_normalize_pzp_path(self):
        self.assertEqual(
            'https://puzz.link/p?roma/3/3/70og4a322c5',
            GameRegistry.normalize_url('http://pzv.jp/p?roma/3/3/70og4a322c5'),
        )

    def test_normalize_pzp_phtml_path(self):
        self.assertEqual(
            'https://puzz.link/p?akari/7/7/zzo',
            GameRegistry.normalize_url('http://pzv.jp/p.html?akari/7/7/zzo'),
        )

    def test_normalize_pzp_https_scheme(self):
        self.assertEqual(
            'https://puzz.link/p?sashigane/5/5/jm.o3khkgojm4',
            GameRegistry.normalize_url('https://pzv.jp/p?sashigane/5/5/jm.o3khkgojm4'),
        )

    def test_normalize_pzp_without_query(self):
        self.assertEqual('https://puzz.link/p', GameRegistry.normalize_url('http://pzv.jp/p'))

    def test_normalize_keeps_canonical_url(self):
        url = 'https://puzz.link/p?roma/3/3/70og4a322c5'
        self.assertEqual(url, GameRegistry.normalize_url(url))

    def test_normalize_keeps_other_domains(self):
        url = 'https://gridpuzzle.com/clouds/2674y'
        self.assertEqual(url, GameRegistry.normalize_url(url))


class GameRegistryRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from Run.UrlPatternMatcher import UrlPatternMatcher
        UrlPatternMatcher()

    def test_pzvjp_roma_url_routes_to_puzzlink_provider(self):
        _, provider, _ = GameRegistry.get_components_for_url('http://pzv.jp/p?roma/3/3/70og4a322c5')
        self.assertIs(provider, PuzzLinkRomaGridProvider)

    def test_pzvjp_phtml_ayeheya_url_routes_to_puzzlink_provider(self):
        _, provider, _ = GameRegistry.get_components_for_url(
            'http://pzv.jp/p.html?ayeheya/11/11/j7j1j1h1hi0i0i0i0papap0v003o03vvs000003vu000g3q3g3j'
        )
        self.assertIs(provider, PuzzLinkAyeheyaGridProvider)


class GameComponentFactoryNormalizationTests(unittest.IsolatedAsyncioTestCase):
    @patch('GridProviders.PuzzLink.PuzzLinkRomaGridProvider.PuzzLinkRomaGridProvider.get_grid', new_callable=AsyncMock)
    async def test_factory_feeds_normalized_url_to_grid_provider(self, mock_get_grid):
        mock_get_grid.return_value = ('grid_data', None, None)
        factory = GameComponentFactory()
        _, _, _, _, _ = await factory.create_components_from_url('http://pzv.jp/p?roma/3/3/70og4a322c5')
        self.assertEqual('https://puzz.link/p?roma/3/3/70og4a322c5', mock_get_grid.await_args.args[0])


if __name__ == '__main__':
    unittest.main()
