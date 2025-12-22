from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.Sudoku.Sudoku.SudokuSolver import SudokuSolver
from GridProviders.GridPuzzle.Base.GridPuzzleProvider import GridPuzzleProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleSudokuGridProvider(PlaywrightGridProvider, GridPuzzleProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url)
        matrix = self._get_grid_data(html_page)
        return Grid(matrix)

    @staticmethod
    def _get_grid_data(html_page: str) -> list[list]:
        soup = BeautifulSoup(html_page, 'html.parser')
        
        cells = soup.find_all('div', class_='g_cell')
        
        if not cells:
            raise ValueError("No grid cells found in HTML")
        
        total_cells = len(cells)
        size = int(total_cells ** 0.5)
        
        matrix = []
        for r in range(size):
            row = []
            for c in range(size):
                cell_index = r * size + c
                cell = cells[cell_index]
                val = cell.get('data-val', '')
                
                if val and val.isdigit():
                    row.append(int(val))
                else:
                    row.append(SudokuSolver.empty)
            matrix.append(row)
        
        return matrix

