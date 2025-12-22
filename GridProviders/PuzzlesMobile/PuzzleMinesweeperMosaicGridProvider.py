import math

from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Puzzles.Minesweeper.MinesweeperSolver import MinesweeperSolver
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleMinesweeperMosaicGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        page = await self.open_page(browser, url)
        await self.new_game(page, 'div.cell')
        numbers_divs = await page.query_selector_all('div.number')
        numbers = [int(inner_text) if (inner_text := await number_div.inner_text()) else MinesweeperSolver.empty for number_div in numbers_divs]
        cells_count = len(numbers)
        side = int(math.sqrt(cells_count))
        matrix = []
        for i in range(0, cells_count, side):
            matrix.append(numbers[i:i + side])
        return Grid(matrix)
