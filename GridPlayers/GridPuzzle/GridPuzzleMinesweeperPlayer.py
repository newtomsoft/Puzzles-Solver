from GridPlayers.PlaywrightPlayer import PlaywrightPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class GridPuzzleMinesweeperPlayer(PuzzlesMobilePlayer, PlaywrightPlayer):
    game_name = "minesweeper"
    async def play(self, solution):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")
        for position in [position for position, value in solution if value]:
            index = position.r * solution.columns_number + position.c
            await cells[index].click()

        await self.close()
        self._process_video(video, rectangle, 0)
