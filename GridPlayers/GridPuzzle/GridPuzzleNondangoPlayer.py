import asyncio

from PuzzleSolver.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer
from GridPlayers.Base.PlayStatus import PlayStatus


class GridPuzzleNondangoPlayer(PlaywrightPlayer):
    game_name = "nondango"

    async def play(self, solution: Grid) -> PlayStatus:
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")
        for position, value in solution:
            if value != 1:
                continue
            index = position.r * solution.columns_number + position.c
            cell = cells[index]
            dango = await cell.query_selector("div.dango")
            if dango is None:
                continue
            await dango.click(click_count=1)

        await asyncio.sleep(2)
        await self.close()
        await self._process_video(video, rectangle)
        return PlayStatus.SUCCESS
