from PuzzleSolver.Board.Grid import Grid
from GridPlayers.Base.PlayStatus import PlayStatus
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleAkariPlayer(PlaywrightPlayer):
    game_name = "akari"

    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.p_cell")
        
        for position, solution_value in [(position, solution_value) for position, solution_value in solution if solution_value == 1]:
            index = position.r * solution.columns_number + position.c
            await cells[index].click(force=True)

        await self.close()
        await self._process_video(video, rectangle, 0)
        return PlayStatus.SUCCESS