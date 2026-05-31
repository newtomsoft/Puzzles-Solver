from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Mobiriti.MobiritiSolver import MobiritiSolver
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleMobiritiPlayer(PlaywrightPlayer):
    game_name = "mobiriti"

    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")

        for position, solution_value in solution:
            if solution_value == MobiritiSolver.black:
                index = position.r * solution.columns_number + position.c
                await cells[index].click()

        await self.close()
        await self._process_video(video, rectangle, 0)
