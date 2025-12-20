from Domain.Board.LinearPathGrid import LinearPathGrid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleNumberChainPlayer(PlaywrightPlayer):
    game_name = "number_chain"
    async def play(self, solution: LinearPathGrid):
        cell_height, cell_width, page, x0, y0 = await self._get_canvas_data(solution.columns_number, solution.rows_number)
        video, rectangle = await self._get_data_video_viewport(page)

        await page.mouse.move(x0 + cell_width / 2 + solution.path[0].c * cell_width, y0 + cell_height / 2 + solution.path[0].r * cell_height)
        await page.mouse.down()
        for position in solution.path[1:]:
            await page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height / 2 + position.r * cell_height)
        await page.mouse.up()

        await self.close()
        self._process_video(video, rectangle)
