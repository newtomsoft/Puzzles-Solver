import asyncio

from Domain.Board.Grid import Grid
from GridPlayers.PuzzlesMobile.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer
from GridPlayers.Base.PlayStatus import PlayStatus


class PuzzleKakuroPlayer(PuzzlesMobilePlayer):
    async def play(self, solution) -> PlayStatus:
        solution = Grid([line + [0] for line in solution.matrix])
        page = self.browser.pages[0]
        cells = page.locator(".cell")

        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if value:
                await cells.nth(index).click()
                await page.keyboard.press(str(value))

        await asyncio.sleep(2)
        result = await self.submit_score(page)
        await asyncio.sleep(3)

        return result
