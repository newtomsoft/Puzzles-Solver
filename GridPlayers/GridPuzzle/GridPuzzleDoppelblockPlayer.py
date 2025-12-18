from Domain.Board.Grid import Grid
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleDoppelblockPlayer(PlaywrightPlayer):
    game_name = "doppelblock"

    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")
        for position, solution_value in solution:
            index = position.r * solution.columns_number + position.c
            if (await cells[index].text_content()).strip() == str(solution_value):
                continue
            await cells[index].click()
            if solution_value == 0:
                await page.keyboard.press('b')
            else:
                await page.keyboard.press(str(solution_value))
        await self.close()
        self._process_video(video, rectangle, 0)
