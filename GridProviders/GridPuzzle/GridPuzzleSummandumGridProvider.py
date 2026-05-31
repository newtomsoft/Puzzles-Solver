from bs4 import BeautifulSoup
from rebrowser_playwright.async_api import BrowserContext
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleSummandumGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, "#puzzle")
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str) -> Grid:
        soup = BeautifulSoup(html_page, 'html.parser')
        table = soup.find('table', id='gridTable')
        if not table:
            # Fallback to old method if table is not found (though sample uses table)
            soup, row_count, column_count, matrix, matrix_cells = self._get_grid_data(html_page)
            for i, cell in enumerate(matrix_cells):
                row = i // column_count
                col = i % column_count
                text = cell.get('data-val', '').strip()
                if not text:
                    text = cell.get_text().strip()
                try:
                    matrix[row][col] = int(text)
                except (ValueError, TypeError):
                    matrix[row][col] = None
            return Grid(matrix)

        rows = table.find('tbody').find_all('tr')
        matrix = []
        for tr in rows:
            row_data = []
            cells = tr.find_all('td', class_='cell_txt')
            for td in cells:
                text = td.get_text(strip=True)
                try:
                    row_data.append(int(text))
                except (ValueError, TypeError):
                    row_data.append(None)
            matrix.append(row_data)

        return Grid(matrix)
