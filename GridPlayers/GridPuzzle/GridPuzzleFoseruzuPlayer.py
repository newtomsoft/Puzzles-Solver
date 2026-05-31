from Domain.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleFoseruzuPlayer(PlaywrightPlayer):
    game_name = "foseruzu"

    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)
        cells = await page.query_selector_all("div.g_cell")
        for position, value in solution:
            if value == 0:
                continue
            index = position.r * solution.columns_number + position.c
            cell = cells[index]
            if value & 1:
                await cell.click(position={"x": 36, "y": 20})
            if value & 2:
                await cell.click(position={"x": 20, "y": 36})
        await self.close()
        await self._process_video(video, rectangle, 0)
