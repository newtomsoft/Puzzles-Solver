import asyncio

from Domain.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer
from GridPlayers.Base.PlayStatus import PlayStatus


class GridPuzzleYinYangPlayer(PlaywrightPlayer):
    async def play(self, solution: Grid) -> PlayStatus:
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")

        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            cell = cells[index]

            is_readonly = await cell.get_attribute("data-readonly") == "y"
            if is_readonly:
                continue

            current_val = await cell.get_attribute("data-val") or ""

            # Cycle on gridpuzzle.com: empty -> black (0) -> white (1) -> empty
            # We need to reach the target value from the current value
            if value == 0 and current_val != "b":  # Target: black
                if current_val == "w":
                    await cell.click(click_count=2)
                else:
                    await cell.click()
            elif value == 1 and current_val != "w":
                if current_val == "b":
                    await cell.click()
                else:
                    await cell.click(click_count=2)

        await asyncio.sleep(1)
        await self.close()
        await self._process_video(video, rectangle, 0)

        return PlayStatus.SUCCESS
