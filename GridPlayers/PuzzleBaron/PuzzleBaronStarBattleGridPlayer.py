import asyncio

from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class PuzzleBaronStarBattlePlayer(PlaywrightPlayer):
    async def play(self, solution):
        page = self.browser.pages[0]
        grid_box_divs = await page.query_selector_all('div.box')

        for position, _ in [(position, value) for position, value in solution if value]:
            index = solution.get_index_from_position(position)
            await grid_box_divs[index].click(click_count=2)

        await asyncio.sleep(20)
