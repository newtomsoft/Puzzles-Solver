from Domain.Board.IslandsGrid import IslandGrid
from GridPlayers.GridPuzzle.Base.GridPuzzleCanvasPlayer import GridPuzzleCanvasPlayer
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleCanvasLoopAndBlackCellsPlayer(PlaywrightPlayer, GridPuzzleCanvasPlayer):
    async def play(self, solution: IslandGrid):
        cell_height, cell_width, page, x0, y0 = await self._get_canvas_data(solution.columns_number, solution.rows_number)
        video, rectangle = await self._get_data_video_viewport(page)

        await self.mark_black_cells(cell_height, cell_width, page, solution, x0, y0)
        await self._draw_loop(cell_height, cell_width, page, solution, x0, y0)

        await self.close()
        self._process_video(video, rectangle)

    async def mark_black_cells(self, cell_height, cell_width, page, solution, x0, y0):
        for position in [position for position, value in solution if value == "■"]:
            await page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height / 2 + position.r * cell_height)
            await self.mouse_click(page)


