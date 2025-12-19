import math

from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleKakuroGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        await page.goto(url, wait_until='domcontentloaded')
        await self.new_game(page)
        html_page = await page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        cell_divs = soup.find_all('div', class_='cell')
        flat_matrix: list[list | int] = [0] * len(cell_divs)
        for i, cell_div in enumerate(cell_divs):
            classes = cell_div.get('class', [])
            if 'wall' in classes:
                flat_matrix[i] = [0, 0]
                continue
            task_horizontal = cell_div.select_one('div.task-horizontal')
            task_vertical = cell_div.select_one('div.task-vertical')
            if not task_horizontal and not task_vertical:
                continue
            horizontal_value = int(task_horizontal.get_text()) if task_horizontal else 0
            vertical_value = int(task_vertical.get_text()) if task_vertical else 0
            flat_matrix[i] = [horizontal_value, vertical_value]

        cells_count = len(flat_matrix)
        row_count = int(math.sqrt(cells_count))
        column_count = row_count
        matrix = [flat_matrix[i:i + column_count] for i in range(0, cells_count, row_count)]
        self.remove_margins_cells(matrix)

        return Grid(matrix)

    @staticmethod
    def remove_margins_cells(matrix):
        matrix.pop()
        matrix[:] = [row[:-1] for row in matrix]
