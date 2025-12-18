from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleStr8tsGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, "#puzzle_main")
        _, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        black_matrix = [[False for _ in range(column_count)] for _ in range(row_count)]
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            if 'b_cell' in cell.get('class'):
                black_matrix[row][col] = True
            text = cell.get_text().strip()
            if text:
                matrix[row][col] = int(text)

        return Grid(matrix), Grid(black_matrix)


