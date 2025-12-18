import asyncio

from GridPlayers.PlaywrightPlayer import PlaywrightPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleBimaruPlayer(PuzzlesMobilePlayer, PlaywrightPlayer):
    async def play(self, solution):
        page = self.browser.pages[0]
        cells = page.locator(".cell:not(.task):not(.ship)")

        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if value:
                await cells.nth(index).click()

        await self.submit_score(page)
        await asyncio.sleep(3)
