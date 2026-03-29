from Domain.Puzzles.KinKonKan.KinKonKanSolver import KinKonKanSolver
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleKinKonKanPlayer(PlaywrightPlayer):
    game_name = "kin-kon-kan"
    slash = KinKonKanSolver.slash
    backslash = KinKonKanSolver.backslash

    async def play(self, solution):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")
        cols = solution.columns_number

        for position, val in ((item, val) for item, val in solution if val != "."):
            index = position.r * cols + position.c
            cell = cells[index]

            if val == self.backslash:
                await cell.click(click_count=2)

            elif val == self.slash:
                await cell.click(click_count=3)

        await self.close()
        await self._process_video(video, rectangle, 0)
