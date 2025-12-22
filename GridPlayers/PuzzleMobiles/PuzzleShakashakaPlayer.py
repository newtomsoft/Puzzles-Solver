import asyncio

from Domain.Board.Grid import Grid
from Domain.Puzzles.Shakashaka.ShakashakaSolver import ShakashakaCellType
from GridPlayers.PuzzleMobiles.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer
from GridPlayers.PuzzleMobiles.Base.PlayStatus import PlayStatus


class PuzzleShakashakaPlayer(PuzzlesMobilePlayer):
    async def play(self, solution: Grid) -> PlayStatus:
        page = self.browser.pages[0]

        cells = page.locator('div.cell, div.shakashaka-task-cell')
        box = await cells.nth(0).bounding_box()
        w = box["width"]
        h = box["height"]

        for position, value in [(pos, val) for pos, val in solution if val not in {ShakashakaCellType.BLACK_FULL, ShakashakaCellType.WHITE_FULL}]:
            idx = position.r * solution.columns_number + position.c
            cell = cells.nth(idx)
            if value == ShakashakaCellType.WHITE_BR:
                await cell.click(position={"x": w * 0.15, "y": h * 0.15})
                continue
            if value == ShakashakaCellType.WHITE_BL:
                await cell.click(position={"x": w * 0.85, "y": h * 0.15})
                continue
            if value == ShakashakaCellType.WHITE_TL:
                await cell.click(position={"x": w * 0.85, "y": h * 0.85})
                continue
            await cell.click(position={"x": w * 0.15, "y": h * 0.85})

        await asyncio.sleep(2)
        result = await self.submit_score(page)
        await asyncio.sleep(3)

        return result
