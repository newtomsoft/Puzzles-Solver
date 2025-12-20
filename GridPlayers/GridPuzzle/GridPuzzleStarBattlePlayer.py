from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleStarBattlePlayer(PlaywrightPlayer):
    game_name = "starBattle"
    async def play(self, solution):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")
        for position_index in [position.r * solution.columns_number + position.c for position, value in solution if value]:
            await cells[position_index].click(click_count=2)

        await self.close()
        self._process_video(video, rectangle, 0)
