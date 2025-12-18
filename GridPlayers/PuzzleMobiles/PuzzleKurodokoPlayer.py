import asyncio
from typing import Literal

from Domain.Board.Grid import Grid
from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleKurodokoPlayer(PuzzlesMobilePlayer):
    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        url = page.url
        button: Literal['left', 'right'] = 'right' if 'puzzles-mobile' in url else 'left'

        cells = page.locator(".cell, .task-cell")
        for position in [position for position, value in solution if not value]:
            index = position.r * solution.columns_number + position.c
            await cells.nth(index).click(button=button)

        await self.submit_score(page)
        await asyncio.sleep(3)

