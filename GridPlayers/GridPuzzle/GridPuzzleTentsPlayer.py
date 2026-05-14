from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleTentsPlayer(PlaywrightPlayer):
    game_name = "tents"

    async def play(self, solution):
        page = self.browser.pages[0]
        cells = await page.query_selector_all("div.g_cell")
        for position, value in [(position, value) for position, value in solution if value]:
            index = position.r * solution.columns_number + position.c
            await cells[index].click(click_count=2)
        await self.close()
