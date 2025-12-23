import asyncio

from Domain.Board.Direction import Direction
from Domain.Board.IslandsGrid import IslandGrid
from GridPlayers.PuzzlesMobile.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer
from GridPlayers.Base.PlayStatus import PlayStatus


class PuzzleShingokiPlayer(PuzzlesMobilePlayer):
    async def play(self, solution: IslandGrid) -> PlayStatus:
        page = self.browser.pages[0]
        horizontals = page.locator(".loop-horizontal")
        verticals = page.locator(".loop-vertical")
        for island in solution.islands.values():
            index_horizontal = island.position.r * (solution.columns_number - 1) + island.position.c
            index_vertical = island.position.r * solution.columns_number + island.position.c
            if Direction.right() in island.direction_position_bridges:
                box = await horizontals.nth(index_horizontal).bounding_box()
                await page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
                await page.mouse.down()
                await page.mouse.up()
            if Direction.down() in island.direction_position_bridges:
                box = await verticals.nth(index_vertical).bounding_box()
                await page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
                await page.mouse.down()
                await page.mouse.up()
        await asyncio.sleep(2)
        result = await self.submit_score(page)
        await asyncio.sleep(3)

        return result
