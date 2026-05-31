from rebrowser_playwright.async_api import BrowserContext

from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleStarBattleGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page, url)

    def get_grid_from_html(self, html_page: str, url: str = ''):
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)

        opened_grid = self.make_opened_grid(row_count, column_count, matrix_cells)

        regions_grid = RegionsGrid.from_opened_grid(opened_grid)
        stars_count = 2 if 'starbattle2' in url else 1
        return regions_grid, stars_count
