import math
from typing import Any

from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleThermometersGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        page = await self.open_page(browser, url)
        await self.new_game(page)
        html_page = await page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        cell_divs = soup.find_all('div', class_='cell')
        matrix_cells = sorted(
            [cell_div for cell_div in cell_divs if 'selectable' in cell_div.get('class', [])],
            key=lambda div: (int(div['style'].split('top:')[1].split('px')[0]), int(div['style'].split('left:')[1].split('px')[0]))
        )
        cells_count = len(matrix_cells)
        row_count = int(math.sqrt(cells_count))
        column_count = row_count
        cell_types = {'start': 's', 'straight': 'l', 'curve': 'c', 'end': 'e'}
        rs = {'r1': '1', 'r2': '2', 'r3': '3'}
        matrix = [['' for _ in range(column_count)] for _ in range(row_count)]
        for i, cell in enumerate(matrix_cells):
            row = i // column_count
            col = i % column_count
            cell_classes = cell.get('class', [])
            cell_type = [cell_types[key] for key in cell_classes if key in cell_types.keys()][0]
            r = [rs[key] for key in cell_classes if key in rs.keys()]
            r = r[0] if len(r) > 0 else '4' if cell_type != 'l' else '2'
            matrix[row][col] = f'{cell_type}{r}'

        task_cells = [cell_div for cell_div in cell_divs if 'task' in cell_div.get('class', [])]
        fulls = [int(cell_div.text) for cell_div in task_cells]
        full_by_column_row = {'column': fulls[:row_count], 'row': fulls[row_count:]}

        return Grid(matrix), full_by_column_row
