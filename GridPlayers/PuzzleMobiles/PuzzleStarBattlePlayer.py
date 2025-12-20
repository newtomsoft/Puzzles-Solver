import asyncio

from GridPlayers.PuzzleMobiles.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleStarBattlePlayer(PuzzlesMobilePlayer):
    async def play(self, solution):
        page = self.browser.pages[0]
        cells = page.locator(".cell, .task-cell")
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if value:
                await cells.nth(index).click()
        await asyncio.sleep(2)
        await self.submit_score(page)
        await asyncio.sleep(3)
