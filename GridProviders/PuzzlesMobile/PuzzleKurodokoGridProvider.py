from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.Kurodoko.KurodokoSolver import KurodokoSolver
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleKurodokoGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        page = await self.open_page(browser, url)
        await self.new_game(page, 'div.cell')
        html_page = await page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        cell_divs = soup.find_all('div', class_='cell')

        if not cell_divs:
             raise ValueError("No cells found. Check selector.")

        rows_number = sum(1 for cell in cell_divs if 'left: 1px' in cell['style'])
        columns_number = sum(1 for cell in cell_divs if 'top: 1px' in cell['style'])
        cells_count = len(cell_divs)

        if columns_number == 0 or rows_number == 0:
            raise ValueError(f"Could not determine dimensions. Found {cells_count} cells.")

        if columns_number * rows_number != cells_count:
             filtered_cells = [c for c in cell_divs if 'top:' in c['style'] and 'left:' in c['style']]
             if len(filtered_cells) != cells_count:
                 cell_divs = filtered_cells
                 rows_number = sum(1 for cell in cell_divs if 'left: 1px' in cell['style'])
                 columns_number = sum(1 for cell in cell_divs if 'top: 1px' in cell['style'])
                 cells_count = len(cell_divs)

             if columns_number * rows_number != cells_count:
                 raise ValueError(f"Grid parsing error: {rows_number}x{columns_number} != {cells_count}")

        numbers = [int(inner_text) if (inner_text := cell_div.get_text()) else KurodokoSolver.empty for cell_div in cell_divs]

        matrix = []
        for i in range(0, cells_count, columns_number):
            matrix.append(numbers[i:i + columns_number])

        return Grid(matrix)
