import asyncio

from GridPlayers.PuzzleMobiles.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleAquariumPlayer(PuzzlesMobilePlayer):
    async def play(self, solution):
        page = self.browser.pages[0]
        cells = await page.query_selector_all("div.selectable")
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if value:
                await cells[index].click()

        await asyncio.sleep(2)
        await self.submit_score(page)
        await asyncio.sleep(3)
