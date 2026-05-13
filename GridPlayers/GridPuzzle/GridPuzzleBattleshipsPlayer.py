from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleBattleshipsPlayer(PlaywrightPlayer):
    game_name = "battleships"

    async def play(self, solution):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div#puzzle-main > div.cell")
        if not cells:
            cells = await page.query_selector_all("div.cell")

        for position, value in solution:
            if value <= 0:
                continue
            cell_id = position.r * solution.columns_number + position.c
            if cell_id >= len(cells):
                continue

            classes = await cells[cell_id].get_attribute("class")
            if classes and "tip_cell" in classes:
                continue

            await cells[cell_id].click(click_count=2)

        await self.close()
        await self._process_video(video, rectangle, 0)
