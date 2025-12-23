import asyncio

from GridPlayers.PuzzlesMobile.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer
from GridPlayers.Base.PlayStatus import PlayStatus


class PuzzleLitsPlayer(PuzzlesMobilePlayer):
    async def play(self, solution) -> PlayStatus:
        page = self.browser.pages[0]
        cells = await page.query_selector_all("div.selectable")
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if value:
                await cells[index].click()

        await asyncio.sleep(2)
        result = await self.submit_score(page)
        await asyncio.sleep(3)

        return result