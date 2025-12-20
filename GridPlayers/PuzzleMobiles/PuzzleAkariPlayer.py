import asyncio

from GridPlayers.PuzzleMobiles.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer
from GridPlayers.PuzzleMobiles.Base.SubmissionStatus import SubmissionStatus


class PuzzleAkariPlayer(PuzzlesMobilePlayer):
    async def play(self, solution) -> SubmissionStatus:
        page = self.browser.pages[0]
        cells = await page.query_selector_all("div.cell, div.light-up-task-cell")
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if value:
                await cells[index].click()

        result = await self.submit_score(page)
        await asyncio.sleep(3)

        return result
