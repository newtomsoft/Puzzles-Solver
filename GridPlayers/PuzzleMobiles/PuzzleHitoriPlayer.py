import asyncio

from GridPlayers.PuzzleMobiles.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleHitoriPlayer(PuzzlesMobilePlayer):
    async def play(self, solution):
        page = self.browser.pages[0]
        cells = await page.query_selector_all("div.cell.selectable")
        for index, _ in [(solution.get_index_from_position(position), value) for position, value in solution if not value]:
            await cells[index].click()

        await self.submit_score(page)
        await asyncio.sleep(3)
