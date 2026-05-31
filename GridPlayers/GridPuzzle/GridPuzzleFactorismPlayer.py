from PuzzleSolver.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer

class GridPuzzleFactorismPlayer(PlaywrightPlayer):
    game_name = "factorism"

    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        col_header_inputs = await page.query_selector_all("table#gridTable thead th.cell_val")
        row_header_inputs = await page.query_selector_all("table#gridTable tbody th.cell_val")

        for c in range(min(len(col_header_inputs), solution.columns_number - 1)):
            val = solution[0, c + 1]
            if val is not None:
                current_val = await col_header_inputs[c].inner_text()
                if current_val.strip() != str(val):
                    await col_header_inputs[c].click()
                    for char in str(val):
                        await page.keyboard.press(char)

        for r in range(min(len(row_header_inputs), solution.rows_number - 1)):
            val = solution[r + 1, 0]
            if val is not None:
                current_val = await row_header_inputs[r].inner_text()
                if current_val.strip() != str(val):
                    await row_header_inputs[r].click()
                    for char in str(val):
                        await page.keyboard.press(char)

        await self.close()
        await self._process_video(video, rectangle, 0)
