import asyncio
from typing import Literal

from Domain.Board.Grid import Grid
from GridPlayers.PuzzleMobiles.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer
from GridPlayers.Base.PlayStatus import PlayStatus


class PuzzleKurodokoPlayer(PuzzlesMobilePlayer):
    async def play(self, solution: Grid) -> PlayStatus:
        page = self.browser.pages[0]
        button_position: Literal["left", "right"] = "right" if "puzzles-mobile" in page.url else "left"

        cells = page.locator(".cell, .task-cell")

        for index in (solution.get_index_from_position(position) for position, value in solution if not value):
            await cells.nth(index).click(button=button_position)

        await asyncio.sleep(2)
        result = await self.submit_score(page)
        await asyncio.sleep(3)

        return result
