from typing import Any

from playwright.async_api import BrowserContext

from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzLink.PuzzLinkGridProvider import PuzzLinkGridProvider


class PuzzLinkAyeheyaGridProvider(PlaywrightGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        if len(browser.pages) == 0:
            page = await browser.new_page()
        else:
            page = browser.pages[0]

        await page.goto(url)
        await page.wait_for_selector("#divques svg", state="visible")
        await page.wait_for_function("typeof ui !== 'undefined' && ui.puzzle && ui.puzzle.board")

        ir = PuzzLinkGridProvider.decode_url(url)
        number_grid = PuzzLinkGridProvider.build_number_grid(ir)
        region_grid = PuzzLinkGridProvider.build_region_grid(ir)

        return number_grid, region_grid
