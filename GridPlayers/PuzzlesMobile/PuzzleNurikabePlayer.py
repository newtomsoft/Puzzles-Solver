import asyncio

from GridPlayers.PuzzlesMobile.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer
from GridPlayers.Base.PlayStatus import PlayStatus


class PuzzleNurikabePlayer(PuzzlesMobilePlayer):
    async def play(self, solution) -> PlayStatus:
        page = self.browser.pages[0]
        cells = await page.query_selector_all("div.board-back > div")
        for position, value in [(position, value) for (position, value) in solution if value]:
            index = position.r * solution.columns_number + position.c
            bounding_box = await cells[index].bounding_box()
            x = bounding_box['x'] + bounding_box['width'] / 2
            y = bounding_box['y'] + bounding_box['height'] / 2
            await page.mouse.move(x, y)
            await page.mouse.down()
            await page.mouse.up()

        await asyncio.sleep(2)
        result = await self.submit_score(page)
        await asyncio.sleep(3)

        return result
