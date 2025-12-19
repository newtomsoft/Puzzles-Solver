from playwright.async_api import BrowserContext

from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileRegionGridProvider import PuzzlesMobileRegionGridProvider


class PuzzleNorinoriGridProvider(PlaywrightGridProvider, PuzzlesMobileRegionGridProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        page = await self.open_page(browser, url)
        await self.new_game(page)
        html_page = await page.content()
        regions_grid = self._scrap_region_grid(html_page)
        return regions_grid
