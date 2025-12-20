import asyncio

from GridPlayers.PuzzleMobiles.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleAkariPlayer(PuzzlesMobilePlayer):
    async def play(self, solution):
        page = self.browser.pages[0]
        cells = await page.query_selector_all("div.cell, div.light-up-task-cell")
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if value:
                await cells[index].click()

        await self.submit_score(page)
        await asyncio.sleep(3)
