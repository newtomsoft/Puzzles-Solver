import asyncio

from Domain.Board.Direction import Direction
from Domain.Board.IslandsGrid import IslandGrid
from GridPlayers.PuzzleMobiles.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer
from GridPlayers.PuzzleMobiles.Base.SubmissionStatus import SubmissionStatus


class PuzzleHashiPlayer(PuzzlesMobilePlayer):
    async def play(self, solution: IslandGrid) -> SubmissionStatus:
        page = self.browser.pages[0]
        cells = page.locator(".bridges-task-cell")
        for index, island in enumerate(solution.islands.values()):
            box = await cells.nth(index).bounding_box()
            for direction, (position, value) in island.direction_position_bridges.items():
                if direction == Direction.down():
                    await page.mouse.move(box['x'] + box['width'] // 2, box['y'] + box['height'] + 5)
                    for _ in range(value):
                        await page.mouse.down()
                        await page.mouse.up()
                elif direction == Direction.right():
                    await page.mouse.move(box['x'] + box['width'] + 5, box['y'] + box['height'] // 2)
                    for _ in range(value):
                        await page.mouse.down()
                        await page.mouse.up()
        result = await self.submit_score(page)
        await asyncio.sleep(3)

        return result
