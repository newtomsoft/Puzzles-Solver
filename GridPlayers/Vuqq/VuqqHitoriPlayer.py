import asyncio

from Domain.Board.Grid import Grid
from GridPlayers.Base.PlayStatus import PlayStatus
from GridPlayers.Vuqq.Base.VuqqPlayer import VuqqPlayer


class VuqqHitoriPlayer(VuqqPlayer):
    async def play(self, grid: Grid) -> PlayStatus:
        page = self.browser.pages[0]
        cells = page.locator('.grid__cell')

        for position in (position for position, value in grid if not value):
            idx = grid.get_index_from_position(position)
            cell = cells.nth(idx)
            await cell.click()

        await asyncio.sleep(2)
        result = await self.get_play_status(page, success_message = "Victoire !")
        await asyncio.sleep(3)

        return result