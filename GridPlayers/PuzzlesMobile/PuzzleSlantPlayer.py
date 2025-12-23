import asyncio

from Domain.Board.Grid import Grid
from GridPlayers.PuzzlesMobile.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer
from GridPlayers.Base.PlayStatus import PlayStatus


class PuzzleSlantPlayer(PuzzlesMobilePlayer):
    async def play(self, solution: Grid) -> PlayStatus:
        page = self.browser.pages[0]
        cell_elements = page.locator('div.cell')

        for position, target_val in solution:
            idx = position.r * solution.columns_number + position.c
            if target_val:
                await cell_elements.nth(idx).click(button="left")
            else:
                await cell_elements.nth(idx).click(button="right")

        await asyncio.sleep(2)
        result = await self.submit_score(page)
        await asyncio.sleep(3)

        return result
