import asyncio

from Domain.Board.Grid import Grid
from GridPlayers.Base.PlayStatus import PlayStatus
from GridPlayers.Vuqq.Base.VuqqPlayer import VuqqPlayer


class VuqqSudokuPlayer(VuqqPlayer):
    async def play(self, solution: Grid) -> PlayStatus:
        page = self.browser.pages[0]

        await page.wait_for_selector('.grid__cell')

        cells = await page.query_selector_all('.grid__cell')
        if len(cells) != 81:
            raise Exception("Grid cells not found during playback")

        numpad_buttons = await page.query_selector_all('.game__controls-numpad span')

        numpad_map = {}
        for btn in numpad_buttons:
            text = await btn.inner_text()
            text = text.strip()
            if text.isdigit():
                numpad_map[int(text)] = btn

        for position, value in solution:
            idx = solution.get_index_from_position(position)
            cell = cells[idx]

            number_span = await cell.query_selector('.number')
            existing_text = ""
            if number_span:
                existing_text = await number_span.inner_text()

            if existing_text.strip():
                continue

            await cell.click()

            if value in numpad_map:
                await numpad_map[value].click()
            else:
                print(f"Warning: Numpad button for {value} not found")

        await asyncio.sleep(2)
        result = await self.get_play_status(page, success_message = "Victoire !")
        await asyncio.sleep(3)

        return result

