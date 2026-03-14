from Domain.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleNumbersPlayer(PlaywrightPlayer):
    async def play(self, solution: Grid, columns_number: int = None):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")
        
        if columns_number is None:
            if hasattr(solution, 'columns_number'):
                columns_number = solution.columns_number
            else:
                columns_number = 0

        for position, solution_value in solution:
            index = position.r * columns_number + position.c
            if index >= len(cells):
                break

            cell = cells[index]

            is_readonly = await cell.get_attribute("data-readonly") == "1"
            if is_readonly:
                continue

            current_value = await cell.get_attribute("data-val")
            if current_value == str(solution_value):
                continue

            await self._fill_cell(page, cell, solution_value)

        await self.close()
        await self._process_video(video, rectangle, 0)

    @staticmethod
    async def _fill_cell(page, cell, value):
        await cell.click()
        await page.keyboard.press(str(value))
