
import unittest
from unittest.mock import MagicMock, patch, AsyncMock

from Domain.Board.Grid import Grid
from GridPlayers.Vuqq.VuqqHitoriPlayer import VuqqHitoriPlayer
from GridProviders.Vuqq.VuqqHitoriGridProvider import VuqqHitoriGridProvider


class VuqqHitoriTests(unittest.IsolatedAsyncioTestCase):
    async def test_provider_scraps_grid(self):
        # Mock browser and page
        mock_page = MagicMock()
        mock_page.goto = AsyncMock()
        mock_page.wait_for_selector = AsyncMock()
        mock_page.wait_for_timeout = AsyncMock()

        mock_browser = MagicMock()
        mock_browser.pages = [mock_page]
        mock_browser.new_page.return_value = mock_page

        # Mock locator
        mock_locator = MagicMock()
        mock_page.locator.return_value = mock_locator

        # Setup grid cells
        # 4x4 grid -> 16 cells
        mock_locator.count = AsyncMock(return_value=16)

        mock_cell = MagicMock()
        # Mock inner_text to return string "5" (async)
        mock_cell.inner_text = AsyncMock(return_value="5")
        mock_locator.nth.return_value = mock_cell

        # Let's simplify:
        provider = VuqqHitoriGridProvider()

        with patch('math.isqrt', return_value=4):
            grid = await provider.scrap_grid(mock_browser, "http://url")

        self.assertEqual(grid.rows_number, 4)
        self.assertEqual(grid.columns_number, 4)
        mock_page.goto.assert_called_with("http://url")

    async def test_player_clicks_cells(self):
        # Mock browser and page
        mock_page = MagicMock()
        mock_browser = MagicMock()
        mock_browser.pages = [mock_page]

        player = VuqqHitoriPlayer(mock_browser)

        # 2x2 grid
        # [False, 1]
        # [2, False]
        grid = Grid([[False, 1], [2, False]])

        mock_cells_locator = MagicMock()
        mock_page.locator.return_value = mock_cells_locator

        mock_cell = MagicMock()
        mock_cells_locator.nth.return_value = mock_cell

        # Setup get_attribute('class') return values
        mock_cell.get_attribute = AsyncMock(return_value="grid__cell") # Empty
        mock_cell.click = AsyncMock()

        await player.play(grid)

        # We expect clicks
        self.assertTrue(mock_cell.click.called)
