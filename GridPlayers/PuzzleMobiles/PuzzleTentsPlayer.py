import asyncio

from GridPlayers.PuzzleMobiles.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleTentsPlayer(PuzzlesMobilePlayer):
    async def play(self, solution):
        page = self.browser.pages[0]
        cells = await page.query_selector_all("div.tents-cell-back > div:not(.print-helper)")
        for position, value in [(position, value) for (position, value) in solution if value]:
            index = position.r * solution.columns_number + position.c
            bounding_box = await cells[index].bounding_box()
            x = bounding_box['x'] + bounding_box['width'] / 2
            y = bounding_box['y'] + bounding_box['height'] / 2
            await page.mouse.move(x, y)
            await page.mouse.down()
            await page.mouse.up()

        await self.submit_score(page)
        await asyncio.sleep(3)
