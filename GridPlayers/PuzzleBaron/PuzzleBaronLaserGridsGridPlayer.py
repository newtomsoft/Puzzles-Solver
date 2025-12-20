import asyncio

from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class PuzzleBaronLaserGridsPlayer(PlaywrightPlayer):
    async def play(self, solution):
        page = self.browser.pages[0]
        grid_box_divs = await page.query_selector_all('div.gridbox')

        for position, _ in [(position, value) for position, value in solution if value]:
            index = solution.get_index_from_position(position)
            await grid_box_divs[index].click()

        await asyncio.sleep(20)
