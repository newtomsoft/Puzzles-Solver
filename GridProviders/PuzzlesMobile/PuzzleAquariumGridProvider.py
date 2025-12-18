from bs4.element import AttributeValueList
from playwright.async_api import BrowserContext

from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileRegionGridProvider import (
    PuzzlesMobileRegionGridProvider,
)


class PuzzleAquariumGridProvider(PlaywrightGridProvider, PuzzlesMobileRegionGridProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_new_html_page(browser, url)
        cell_divs, row_count, soup = self._scrap_grid_data(html_page)
        regions_grid = self._scrap_region_grid(html_page)

        task_cells = [cell_div for cell_div in cell_divs if 'task' in cell_div.get('class', AttributeValueList([]))]
        numbers = [int(cell_div.text) for cell_div in task_cells]
        return regions_grid, numbers
