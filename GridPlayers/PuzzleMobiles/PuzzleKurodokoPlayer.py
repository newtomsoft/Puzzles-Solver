import asyncio
from typing import Literal

from Domain.Board.Grid import Grid
from GridPlayers.PuzzleMobiles.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleKurodokoPlayer(PuzzlesMobilePlayer):
    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        button_position: Literal["left", "right"] = "right" if "puzzles-mobile" in page.url else "left"

        cells = page.locator(".cell, .task-cell")

        for index in (solution.get_index_from_position(position) for position, value in solution if not value):
            await cells.nth(index).click(button=button_position)

        await self.submit_score(page)
        await asyncio.sleep(3)
