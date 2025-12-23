import asyncio

from Domain.Board.Grid import Grid
from Domain.Puzzles.Pipes.PipeShapeTransition import PipeShapeTransition
from GridPlayers.PuzzleMobiles.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer
from GridPlayers.Base.PlayStatus import PlayStatus


class PuzzlePipesPlayer(PuzzlesMobilePlayer):
    async def play(self, solution: Grid[PipeShapeTransition]) -> PlayStatus:
        page = self.browser.pages[0]
        cells = await page.query_selector_all("div.selectable")
        for position, pipe_shape_transition in solution:
            index = position.r * solution.columns_number + position.c
            await cells[index].click(click_count=pipe_shape_transition.clockwise_rotation)

        await asyncio.sleep(2)
        result = await self.submit_score(page)
        await asyncio.sleep(3)

        return result
