from bs4 import BeautifulSoup
from rebrowser_playwright.async_api import BrowserContext

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Mobiriti.MobiritiSolver import MobiritiSolver
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleMobiritiGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, '.g_cell')
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        soup = BeautifulSoup(html_page, 'html.parser')
        
        matrix_cells = soup.find_all('div', class_='g_cell')
        if not matrix_cells:
            return Grid.empty()
        cells_count = len(matrix_cells)
        row_count = int(cells_count**0.5)
        column_count = row_count

        num_matrix = [[None for _ in range(column_count)] for _ in range(row_count)]

        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            
            # Extract number (if it exists, it's inside a circle)
            txt = cell.get_text(strip=True)
            if txt:
                try:
                    num_matrix[row][col] = int(txt)
                except ValueError:
                    num_matrix[row][col] = None
            else:
                num_matrix[row][col] = None

        return Grid(num_matrix)
