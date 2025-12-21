import math

from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class ZipGridProvider(PlaywrightGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        await page.goto(url)
        frame = page.frames[1]
        start_game_button = await frame.wait_for_selector('button:has-text("Commencer une partie")')
        await start_game_button.click()
        game_board = await frame.wait_for_selector('.game-board')
        cells_divs = await game_board.query_selector_all('div.trail-cell')

        numbers = []
        for cell_div in cells_divs:
            text = await cell_div.text_content()
            text = text.strip()
            numbers.append(int(text) if text else 0)

        cells_number = len(cells_divs)
        columns_number = int(math.sqrt(cells_number))
        matrix = []
        for i in range(0, cells_number, columns_number):
            matrix.append(numbers[i:i + columns_number])
        grid = Grid(matrix)

        walls = await self._get_walls(game_board, columns_number)
        grid.set_walls(walls)
        return grid

    @staticmethod
    async def _get_walls(game_board, columns_number):
        wall_right_divs = await game_board.query_selector_all('div.trail-cell-wall--right')
        cell_wall_right_divs = [await wall_right_div.evaluate_handle('node => node.parentElement') for wall_right_div in wall_right_divs]
        cell_wall_right_indexes = [int(await parent.evaluate('node => node.getAttribute("data-cell-idx")')) for parent in cell_wall_right_divs]
        wall_down_divs = await game_board.query_selector_all('div.trail-cell-wall--down')
        cell_wall_down_divs = [await wall_down_div.evaluate_handle('node => node.parentElement') for wall_down_div in wall_down_divs]
        cell_wall_down_indexes = [int(await parent.evaluate('node => node.getAttribute("data-cell-idx")')) for parent in cell_wall_down_divs]
        walls = set()
        for index in cell_wall_right_indexes:
            row = index // columns_number
            column = index % columns_number
            walls.add(frozenset((Position(row, column), Position(row, column + 1))))
        for index in cell_wall_down_indexes:
            row = index // columns_number
            column = index % columns_number
            walls.add(frozenset((Position(row, column), Position(row + 1, column))))
        return walls
