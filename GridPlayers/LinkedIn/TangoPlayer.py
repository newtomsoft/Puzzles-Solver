from Domain.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class TangoPlayer(PlaywrightPlayer):
    game_name = "tango"

    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        frame = page.frames[1]
        board = await frame.wait_for_selector('div.grid-board')
        cells_divs = await board.query_selector_all('div.lotka-cell')

        video, rectangle = await self._get_data_video(frame, '.grid-board', page, 12, 23, 12, 150)

        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            cell = cells_divs[index]
            if await cell.is_enabled():
                await cell.click(click_count=1 if value else 2)

        await self.close(delay_sec=5)
        self._process_video(video, rectangle, 3)
