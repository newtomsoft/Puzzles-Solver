from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class HidokuPlayer(PlaywrightPlayer):
    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        rows = solution.rows_number
        cols = solution.columns_number

        cell_height, cell_width, page, x0, y0 = await self._get_canvas_data(cols, rows)

        for r in range(rows):
            for c in range(cols):
                value = solution[r, c]

                # Calculate center of the cell
                x = x0 + c * cell_width + cell_width / 2
                y = y0 + r * cell_height + cell_height / 2

                await page.mouse.click(x, y)
                await page.keyboard.type(str(value))
