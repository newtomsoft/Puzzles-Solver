from GridPlayers.PlaywrightPlayer import PlaywrightPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class GridPuzzleNo4InARowPlayer(PuzzlesMobilePlayer, PlaywrightPlayer):
    game_name = "no4InARow"
    async def play(self, solution):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")
        previous_value = False
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            class_attr = await cells[index].get_attribute('class')
            if 'x1' in class_attr or 'o1' in class_attr:
                continue
            if value == previous_value:
                await cells[index].click()
            else:
                await cells[index].click(click_count=2)
            previous_value = value

        await self.close()
        self._process_video(video, rectangle, 0)
