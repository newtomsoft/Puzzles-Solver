from PuzzleSolver.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleSutoretoPlayer(PlaywrightPlayer):
    game_name = "sutoreto"
    async def play(self, solution: tuple[Grid, Grid]):
        grid_solution, grid_blank = solution
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")
        for position, solution_value in [(position, grid_solution[position]) for position, value in grid_blank if value]:
            index = position.r * grid_solution.columns_number + position.c
            await cells[index].click()
            await page.keyboard.press(str(solution_value))

        await self.close()
        await self._process_video(video, rectangle, 0)
