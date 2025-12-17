import asyncio

from Domain.Board.Grid import Grid
from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleSlantPlayer(PuzzlesMobilePlayer):
    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        cell_elements = page.locator('div.cell')

        for position, target_val in solution:
            idx = position.r * solution.columns_number + position.c
            if target_val:
                await cell_elements.nth(idx).click(button="left")
            else:
                await cell_elements.nth(idx).click(button="right")

        await self.submit_score(page)
        await asyncio.sleep(3)
