from playwright.sync_api import BrowserContext

from Domain.Board.RegionsGrid import RegionsGrid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleStarBattleGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        html_page = self.get_html(browser, url)
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)

        opened_grid = self.make_opened_grid(row_count, column_count, matrix_cells)

        regions_grid = RegionsGrid.from_opened_grid(opened_grid)
        stars_count = 2 if 'starbattle2' in url else 1
        return regions_grid, stars_count
