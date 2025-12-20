import asyncio

from GridPlayers.PuzzleMobiles.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer
from GridPlayers.PuzzleMobiles.Base.SubmissionStatus import SubmissionStatus


class PuzzleMinesweeperPlayer(PuzzlesMobilePlayer):
    async def play(self, solution) -> SubmissionStatus:
        page = self.browser.pages[0]
        cells = await page.query_selector_all("div.cell.selectable")
        for index in [solution.get_index_from_position(position) for position, value in solution if value]:
            await cells[index].click(button="right")

        await asyncio.sleep(2)
        result = await self.submit_score(page)
        await asyncio.sleep(3)

        return result
