from Domain.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleDosunFuwariPlayer(PlaywrightPlayer):
    game_name = "dosun fuwari"

    async def play(self, grid_solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")
        for position, solution_value in [(position, solution_value) for position, solution_value in grid_solution if solution_value]:
            index = position.r * grid_solution.columns_number + position.c
            await cells[index].click(click_count=solution_value)

        await self.close()
        self._process_video(video, rectangle, 0)
