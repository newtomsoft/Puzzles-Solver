import asyncio

from GridPlayers.Base.PlayStatus import PlayStatus
from GridPlayers.Vuqq.Base.VuqqPlayer import VuqqPlayer


class VuqqAkariPlayer(VuqqPlayer):
    async def play(self, solution) -> PlayStatus:
        page = self.browser.pages[0]

        meta = await page.evaluate("window.vuqq_meta")
        if not meta:
            raise Exception("No Vuqq metadata found. GridProvider must run before Player.")

        unique_xs = meta['xs']
        unique_ys = meta['ys']

        for position in (position for position, value in solution if value):
            col_idx = position.c
            row_idx = position.r

            if col_idx < len(unique_xs) and row_idx < len(unique_ys):
                x = unique_xs[col_idx]
                y = unique_ys[row_idx]

                await page.mouse.click(x, y)


        await asyncio.sleep(2)
        result = await self.get_play_status(page, success_selector="#win.alert-success:not([style*='display: none'])")
        await asyncio.sleep(3)

        return result