import asyncio

from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class PuzzleBaronCalcudokuPlayer(PlaywrightPlayer):
    async def play(self, solution):
        page = self.browser.pages[0]
        grid_box_divs = await page.query_selector_all('div.gridbox')

        for position, digit in solution:
            index = solution.get_index_from_position(position)
            await grid_box_divs[index].click()
            await page.keyboard.press(str(digit))

        await asyncio.sleep(20)
