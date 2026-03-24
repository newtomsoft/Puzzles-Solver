from playwright.async_api import BrowserContext

from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleGradesGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)

        grid = self.make_grid(column_count, matrix, matrix_cells)
        left = self.make_left(soup)
        top = self.make_top(soup)
        right = self.make_right(soup)
        bottom = self.make_bottom(soup)
        clues = dict(left=left, top=top, right=right, bottom=bottom)

        return grid, clues


