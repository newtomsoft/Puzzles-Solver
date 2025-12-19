import math

from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.Sudoku.SudokuBaseSolver import SudokuBaseSolver
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleSudokuGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        page = await self.open_page(browser, url)
        await self.new_game(page, 'div.number')
        numbers_divs = await page.query_selector_all('div.number')
        numbers_str = [inner_text if (inner_text := await number_div.inner_text()) else SudokuBaseSolver.empty for number_div in numbers_divs]
        cells_count = len(numbers_str)
        side = int(math.sqrt(cells_count))
        conversion_base = side + 1
        numbers = [int(number, conversion_base) if number != SudokuBaseSolver.empty else SudokuBaseSolver.empty for number in numbers_str]
        matrix = []
        for i in range(0, cells_count, side):
            matrix.append(numbers[i:i + side])
        return Grid(matrix)
