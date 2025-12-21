from playwright.async_api import BrowserContext

from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileRegionGridProvider import PuzzlesMobileRegionGridProvider


class PuzzleLitsGridProvider(PlaywrightGridProvider, PuzzlesMobileRegionGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        page = await self.open_page(browser, url)
        await page.wait_for_selector('div.cell')
        await PuzzlesMobileRegionGridProvider.new_game(page)
        html_page = await page.content()
        return self._scrap_region_grid(html_page)
