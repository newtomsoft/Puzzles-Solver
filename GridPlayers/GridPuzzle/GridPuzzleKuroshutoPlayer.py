import asyncio
from PuzzleSolver.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleKuroshutoPlayer(PlaywrightPlayer):
    game_name = "kuroshuto"

    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        # Get all grid cells
        cells = await page.query_selector_all("div.g_cell")

        # Click twice on each black cell
        for i, (position, cell_value) in enumerate(solution):
            if cell_value == '■':
                # Click twice on black cells
                await cells[i].click()
                await asyncio.sleep(0.1)
                await cells[i].click()
                await asyncio.sleep(0.1)

        await asyncio.sleep(1)
        await self.close()
        await self._process_video(video, rectangle, 0)
