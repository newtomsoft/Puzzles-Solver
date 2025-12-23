import asyncio

from Domain.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer
from GridPlayers.PuzzlesMobile.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class VingtMinutesKemaruPlayer(PuzzlesMobilePlayer, PlaywrightPlayer):
    async def play(self, grid_solution: Grid):
        page = self.browser.pages[0]
        cells = await page.query_selector_all("g.grid-cell")
        for position, solution_value in grid_solution:
            index = position.r * grid_solution.columns_number + position.c
            await cells[index].click()
            await page.keyboard.press(str(solution_value))

        await asyncio.sleep(6)
