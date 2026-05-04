from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.Kurotto.KurottoSolver import KurottoSolver
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleKurottoGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        _, _, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            classes = cell.get('class', [])
            if 'num_cell' in classes:
                text = cell.get_text(strip=True)
                if text == '?':
                    matrix[row][col] = KurottoSolver.unknown
                    continue
                matrix[row][col] = int(text)
            else:
                matrix[row][col] = KurottoSolver.empty

        return Grid(matrix)
