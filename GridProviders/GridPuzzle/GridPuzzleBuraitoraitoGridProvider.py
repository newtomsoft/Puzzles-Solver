from rebrowser_playwright.async_api import BrowserContext

from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleBuraitoraitoGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        _, _, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            classes = cell.get('class', [])
            if 'black_cell' in classes:
                data_n = cell.get('data-n', '')
                if data_n:
                    matrix[row][col] = int(data_n)
                else:
                    try:
                        matrix[row][col] = int(cell.get_text(strip=True))
                    except ValueError:
                        matrix[row][col] = 0
            else:
                matrix[row][col] = 0

        return Grid(matrix)
