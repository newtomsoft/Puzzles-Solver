from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleUsotatamiGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        size, pqq, pqq_string = self._extract_gpl_data(html_page)
        pqq_string_list = self._split_to_list(pqq_string, size)

        matrix = []
        for i in range(size):
            row = []
            for j in range(size):
                val = pqq_string_list[i * size + j]
                if val == '.':
                    row.append(None)
                elif val.isdigit():
                    row.append(int(val))
                else:
                    row.append(val)
            matrix.append(row)

        return Grid(matrix)
