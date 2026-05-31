from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Irasuto.IrasutoSolver import IrasutoSolver
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleIrasutoPlayer(PlaywrightPlayer):
    game_name = "irasuto"

    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("#puzzle-main .cell")

        for position, solution_value in solution:
            if solution_value == IrasutoSolver.black:
                index = position.r * solution.columns_number + position.c
                await cells[index].click()

        await self.close()
        await self._process_video(video, rectangle, 0)
