import asyncio

from Domain.Board.Direction import Direction
from GridPlayers.PuzzleMobiles.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleStitchesPlayer(PuzzlesMobilePlayer):
    async def play(self, solution):
        page = self.browser.pages[0]
        cells = page.locator(".cell:not(.task)")
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            box = await cells.nth(index).bounding_box()
            if value == Direction.down():
                await page.mouse.move(box['x'] + box['width'] // 2, box['y'] + box['height'])
                await page.mouse.down()
                await page.mouse.up()
            elif value == Direction.right():
                await page.mouse.move(box['x'] + box['width'], box['y'] + box['height'] // 2)
                await page.mouse.down()
                await page.mouse.up()
        await self.submit_score(page)
        await asyncio.sleep(3)
