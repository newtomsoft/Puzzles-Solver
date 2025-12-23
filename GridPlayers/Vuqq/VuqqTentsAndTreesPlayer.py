import asyncio

from GridPlayers.Base.PlayStatus import PlayStatus
from GridPlayers.Vuqq.Base.VuqqPlayer import VuqqPlayer


class VuqqTentsAndTreesPlayer(VuqqPlayer):
    async def play(self, solution) -> PlayStatus:
        page = self.browser.pages[0]

        meta = await page.evaluate("window.vuqq_meta")
        if not meta:
            raise Exception("No Vuqq metadata found. GridProvider must run before Player.")

        xs = meta["col_xs"]
        ys = meta["row_ys"]

        for position in (position for position, value in solution if value):
            x = xs[position.c]
            y = ys[position.r]
            await page.mouse.click(x, y)

        await asyncio.sleep(2)
        result = await self.get_play_status(page, success_selector=".alert-success")
        await asyncio.sleep(3)

        return result
