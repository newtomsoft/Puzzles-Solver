from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.Sutoreto.SutoretoSolver import SutoretoSolver
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleSutoretoGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, "#puzzle")
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        _, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            if 'b_cell' in cell.get('class', []):
                matrix[row][col] = SutoretoSolver.Black
            else:
                text = cell.get_text().strip()
                if text:
                    try:
                        matrix[row][col] = int(text)
                    except ValueError:
                        matrix[row][col] = None
                else:
                    matrix[row][col] = None

        return Grid(matrix)
