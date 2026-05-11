import asyncio

from Domain.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer
from GridPlayers.Base.PlayStatus import PlayStatus


class GridPuzzleBinairoPlayer(PlaywrightPlayer):
    game_name = "binairo"

    async def play(self, solution: Grid) -> PlayStatus:
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            cell = cells[index]
            data_val = await cell.get_attribute("data-val")
            if data_val == 'b' and value == 1:
                continue
            if data_val == 'w' and value == 0:
                continue
            if data_val == '' and value is None:
                continue
            click_count = 1 if value == 1 else 2 if value == 0 else 0
            if click_count:
                await cell.click(click_count=click_count)

        await asyncio.sleep(2)
        await self.close()
        await self._process_video(video, rectangle)
        return PlayStatus.SUCCESS
