from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleHeyawakePlayer(PlaywrightPlayer):
    game_name = "heyawake"

    async def play(self, solution):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")
        for position, value in solution:
            if not value:
                index = position.r * solution.columns_number + position.c
                await cells[index].click(click_count=2)

        await self.close()
        await self._process_video(video, rectangle, 0)
