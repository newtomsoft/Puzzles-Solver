from playwright.sync_api import BrowserContext

from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileRegionGridProvider import PuzzlesMobileRegionGridProvider


class PuzzleLitsGridProvider(PlaywrightGridProvider, PuzzlesMobileRegionGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        return self._scrap_region_grid(browser, url)
