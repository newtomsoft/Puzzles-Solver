from PuzzleSolver.Board.Grid import Grid
from GridPlayers.Base.PlayStatus import PlayStatus
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzlePutteriaPlayer(PlaywrightPlayer):
    game_name = "putteria"

    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")
        for position, solution_value in [(position, solution[position]) for position, value in solution if value != 0]:
            index = position.r * solution.columns_number + position.c
            cell = cells[index]
            cell_classes = await cell.get_attribute("class") or ""
            if "sys_num" in cell_classes:
                continue
            await cell.click()

        await self.close()
        await self._process_video(video, rectangle, 0)
        return PlayStatus.SUCCESS
