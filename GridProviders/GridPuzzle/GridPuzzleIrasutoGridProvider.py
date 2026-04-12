from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.Irasuto.IrasutoSolver import IrasutoSolver
from GridProviders.GridPuzzle.Base.GridPuzzleTagProvider import GridPuzzleTagProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class GridPuzzleIrasutoGridProvider(PlaywrightGridProvider, GridPuzzleTagProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        html_page = await self.get_html(browser, url, '.puzzle_main')
        return self.get_grid_from_html(html_page)

    def get_grid_from_html(self, html_page: str):
        soup = BeautifulSoup(html_page, 'html.parser')
        container = soup.find('div', class_='puzzle_main')
        if not container:
            return Grid.empty(), Grid.empty()

        matrix_cells = container.find_all('div', class_='cell')
        cells_count = len(matrix_cells)
        row_count = int(cells_count**0.5)
        column_count = row_count

        num_matrix = [[None for _ in range(column_count)] for _ in range(row_count)]
        color_matrix = [[None for _ in range(column_count)] for _ in range(row_count)]

        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            
            # Extract number
            txt = cell.get_text(strip=True)
            if txt:
                try:
                    num_matrix[row][col] = int(txt)
                except ValueError:
                    num_matrix[row][col] = None
            else:
                num_matrix[row][col] = None

            # Extract color
            classes = cell.get('class', [])
            if 'black_cell' in classes:
                color_matrix[row][col] = IrasutoSolver.black
            else:
                color_matrix[row][col] = IrasutoSolver.white

        return Grid(num_matrix), Grid(color_matrix)
