from Domain.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleArrowWebPlayer(PlaywrightPlayer):
    game_name = "arrow web"

    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")
        for position, value in solution:
            if value:
                index = position.r * solution.columns_number + position.c
                await cells[index].click()

        await self.close()
        await self._process_video(video, rectangle, 0)
