import math

from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Board.Pipe import Pipe
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzlePipesGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        page = await self.open_page(browser, url)
        await self.new_game(page, 'div.board-back')
        html_page = await page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        cells_divs = soup.find_all('div', class_='cell')
        rows_number = int(math.sqrt(len(cells_divs)))
        if rows_number * rows_number != len(cells_divs):
            raise ValueError(f'Invalid number of cells computed {len(cells_divs)}')
        columns_number = rows_number
        pipe_classes_to_codes = {
            'pipe3': 'L0', 'pipe6': 'L1', 'pipe12': 'L2', 'pipe9': 'L3',
            'pipe10': 'I0', 'pipe5': 'I1',
            'pipe13': 'T0', 'pipe11': 'T1', 'pipe7': 'T2', 'pipe14': 'T3',
            'pipe1': 'E0', 'pipe2': 'E1', 'pipe4': 'E2', 'pipe8': 'E3',
        }
        matrix = [['' for _ in range(columns_number)] for _ in range(rows_number)]
        for index, dot_div in enumerate(cells_divs):
            row = index // columns_number
            column = index % columns_number
            for pipe_class, code in pipe_classes_to_codes.items():
                if pipe_class in dot_div['class']:
                    matrix[row][column] = Pipe(code)
                    break

        return Grid(matrix)
