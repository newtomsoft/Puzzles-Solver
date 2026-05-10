from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleHitoriPlayer(PlaywrightPlayer):
    game_name = "hitori"

    async def play(self, solution):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.cell")
        for position, _ in [(position, value) for position, value in solution if not value]:
            index = position.r * solution.columns_number + position.c
            await cells[index].click(click_count=2)

        await self.close()
        await self._process_video(video, rectangle, 0)
