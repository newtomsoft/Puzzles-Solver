from time import sleep

from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleTapaPlayer(PuzzlesMobilePlayer):
    async def play(self, solution):
        page = self.browser.pages[0]
        cells = await page.query_selector_all("div.board-back > div")
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            if value:
                await cells[index].click()

        await self.submit_score(page)
        sleep(3)
