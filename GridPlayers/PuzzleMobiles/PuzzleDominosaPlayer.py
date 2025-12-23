import asyncio

from Domain.Board.Direction import Direction
from GridPlayers.PuzzleMobiles.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer
from GridPlayers.Base.PlayStatus import PlayStatus


class PuzzleDominosaPlayer(PuzzlesMobilePlayer):
    async def play(self, solution) -> PlayStatus:
        page = self.browser.pages[0]
        cells = page.locator(".cell")
        unknown_coefficient = 1.25
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            box = await cells.nth(index).bounding_box()
            if value == Direction.down():
                await page.mouse.move(box['x'] + box['width'] / 2, box['y'] + unknown_coefficient * box['height'])
                await page.mouse.down()
                await page.mouse.up()
            elif value == Direction.right():
                await page.mouse.move(box['x'] + unknown_coefficient * box['width'], box['y'] + box['height'] / 2)
                await page.mouse.down()
                await page.mouse.up()
        
        await asyncio.sleep(2)
        result = await self.submit_score(page)
        await asyncio.sleep(3)

        return result
