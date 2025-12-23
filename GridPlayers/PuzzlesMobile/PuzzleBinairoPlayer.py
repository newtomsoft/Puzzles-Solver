import asyncio

from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer
from GridPlayers.Base.PlayStatus import PlayStatus
from GridPlayers.PuzzlesMobile.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleBinairoPlayer(PuzzlesMobilePlayer, PlaywrightPlayer):
    async def play(self, solution) -> PlayStatus:
        page = self.browser.pages[0]
        cells = page.locator(".cell, .task-cell")
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if value:
                await cells.nth(index).click(button="right")
            else:
                await cells.nth(index).click()

        await asyncio.sleep(2)
        result = await self.submit_score(page)
        await asyncio.sleep(3)

        return result
