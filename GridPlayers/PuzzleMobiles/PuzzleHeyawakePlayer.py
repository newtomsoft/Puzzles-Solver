import asyncio

from GridPlayers.PuzzleMobiles.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer
from GridPlayers.PuzzleMobiles.Base.PlayStatus import PlayStatus


class PuzzleHeyawakePlayer(PuzzlesMobilePlayer):
    async def play(self, solution) -> PlayStatus:
        page = self.browser.pages[0]
        cells = await page.query_selector_all("div.selectable")
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if not value:
                await cells[index].click()

        await asyncio.sleep(2)
        result = await self.submit_score(page)
        await asyncio.sleep(3)

        return result
