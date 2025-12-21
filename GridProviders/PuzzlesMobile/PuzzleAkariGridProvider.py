from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleAkariGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        page = await self.open_page(browser, url)
        await self.new_game(page)
        html_page = await page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        cells = soup.find_all('div', class_=['cell', 'light-up-task-cell'])
        values = [-1 if 'wall' in cell['class'] else (int(cell.text) if 'light-up-task-cell' in cell['class'] else None) for cell in cells]
        cells_count = len(values)
        columns_number = sum(1 for cell in cells if 'top: 1px' in cell['style'])
        rows_number = sum(1 for cell in cells if 'left: 1px' in cell['style'])
        if columns_number * rows_number != cells_count:
            raise ValueError("Akari grid parsing error")
        matrix = []
        for r in range(rows_number):
            row = []
            for c in range(columns_number):
                row.append(values[r * columns_number + c])
            matrix.append(row)

        black_cells = {(r, c) for r in range(rows_number) for c in range(columns_number) if matrix[r][c] is not None}
        number_constraints = {(r, c): matrix[r][c] for r in range(rows_number) for c in range(columns_number) if matrix[r][c] is not None and matrix[r][c] != -1}
        return {
            'columns_number': columns_number,
            'rows_number': rows_number,
            'black_cells': black_cells,
            'number_constraints': number_constraints
        }
