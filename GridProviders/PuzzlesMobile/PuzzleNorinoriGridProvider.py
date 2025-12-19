from playwright.async_api import BrowserContext

from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileRegionGridProvider import PuzzlesMobileRegionGridProvider


class PuzzleNorinoriGridProvider(PlaywrightGridProvider, PuzzlesMobileRegionGridProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        await page.goto(url, wait_until='domcontentloaded')
        await self.new_game(page)
        html_page = await page.content()
        regions_grid = self._scrap_region_grid(html_page)
        return regions_grid
