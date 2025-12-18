from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Board.RegionsGrid import RegionsGrid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleFrom1ToXGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        left = [self.extract_value('vl', row_count, soup) for row_count in range(1, row_count + 1)]
        up = [self.extract_value('ht', column_count, soup) for column_count in range(1, column_count + 1)]

        opened_grid = self.make_opened_grid(row_count, column_count, matrix_cells)
        region_grid = RegionsGrid.from_opened_grid(opened_grid)

        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            matrix[row][col] = int(cell.text) if cell.text else 0

        return Grid(matrix), region_grid, left, up

    @staticmethod
    def extract_value(name: str, column_count: int, soup: BeautifulSoup):
        return int(soup.find('div', id=f'{name}_{column_count}').text) if soup.find('div', id=f'{name}_{column_count}').text not in {'\xa0', ''} else 0
