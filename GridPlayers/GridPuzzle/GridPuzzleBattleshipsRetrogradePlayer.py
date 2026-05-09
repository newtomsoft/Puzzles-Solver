import asyncio

from GridPlayers.Base.PlayStatus import PlayStatus
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleBattleshipsRetrogradePlayer(PlaywrightPlayer):
    game_name = "battleships_retrograde"

    async def play(self, solution) -> PlayStatus:
        page = self.browser.pages[0]

        for position, value in solution:
            cell_id = position.r * solution.columns_number + position.c + 1
            state = 's' if value > 0 else 'w'
            await page.evaluate("""(args) => plz.set_cell_val(args[0], args[1])""", [cell_id, state])

        await page.evaluate("""() => plz.get_ship_num()""")
        await asyncio.sleep(1)
        await page.evaluate("""() => plz.save()""")
        await asyncio.sleep(3)

        return PlayStatus.SUCCESS
