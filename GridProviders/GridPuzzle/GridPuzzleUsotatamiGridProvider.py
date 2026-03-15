from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleCanvasProvider import GridPuzzleGridCanvasProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleUsotatamiGridProvider(PlaywrightGridProvider, GridPuzzleGridCanvasProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        pqq_string_list, size = self._get_canvas_data_with_pipe(html_page)

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
