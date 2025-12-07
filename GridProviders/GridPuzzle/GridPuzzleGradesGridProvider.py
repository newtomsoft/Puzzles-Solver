from playwright.sync_api import BrowserContext

from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleGradesGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url)
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)

        grid = self.make_grid(column_count, matrix, matrix_cells)
        left = self.make_left(soup)
        top = self.make_top(soup)
        right = self.make_right(soup)
        bottom = self.make_bottom(soup)
        clues = dict(left=left, top=top, right=right, bottom=bottom)

        return grid, clues


