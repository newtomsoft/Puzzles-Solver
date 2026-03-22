from Domain.Board.Grid import Grid
from Domain.Puzzles.Sutoreto.SutoretoSolver import SutoretoSolver
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleSutoretoPlayer(PlaywrightPlayer):
    game_name = "sutoreto"
    
    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")
        for r in range(solution.rows_number):
            for c in range(solution.columns_number):
                # Skip black cells
                if solution[r, c] == SutoretoSolver.Black:
                    continue
                # Skip if cell already has the correct value
                current_val = await cells[r * solution.columns_number + c].inner_text()
                solution_value = solution[r, c]
                if current_val.strip() != str(solution_value):
                    await cells[r * solution.columns_number + c].click()
                    await page.keyboard.press(str(solution_value))

        await self.close()
        await self._process_video(video, rectangle, 0)
