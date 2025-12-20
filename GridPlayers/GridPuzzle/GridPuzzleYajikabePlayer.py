from Domain.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleYajikabePlayer(PlaywrightPlayer):
    game_name = "yajikabe"
    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.cell")
        for position_index in [position.r * solution.columns_number + position.c for position, value in solution if value]:
            await cells[position_index].click()

        await self.close()
        self._process_video(video, rectangle, 0)
