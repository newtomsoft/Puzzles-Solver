from bs4 import BeautifulSoup
import re
from rebrowser_playwright.async_api import BrowserContext

from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleDeddoanguruGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str) -> Grid:
        pqq_string_list, size = self._get_canvas_data(html_page)
        while len(pqq_string_list) < size * size:
            pqq_string_list.append('')
        matrix = [[-1 for _ in range(size)] for _ in range(size)]
        for i, val in enumerate(pqq_string_list[:size * size]):
            r, c = divmod(i, size)
            if val != '':
                matrix[r][c] = int(val)
        return Grid(matrix)
